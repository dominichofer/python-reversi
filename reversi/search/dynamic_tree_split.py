from enum import IntEnum
import threading
import multiprocessing
from reversi.core import OpenInterval, ClosedInterval

inf_score = +33

class TreeNode:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []

    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_leaf(self):
        return len(self.children) == 0

    def append(self, child):
        child.parent = self
        self.children.append(child)


def traverse_depth_first(node: TreeNode, pre_children_op, post_children_op):
    pre_children_op(node)
    for child in node.children:
        traverse_depth_first(child, pre_children_op, post_children_op)
    post_children_op(node)
    
    
class NodeType(IntEnum):
    PV = 0
    All = 1
    Cut = 2
        

class NodeStatus(IntEnum):
    Unsolved = 0
    Taken = 1
    Solved = 2
    

class SearchNode(TreeNode):
        
    def __init__(self, ply, type: NodeType, pos, window: OpenInterval):
        super().__init__()
        self.ply = ply  # remaining
        self._status = NodeStatus.Unsolved
        self._type = type
        self.pos = pos
        self.window = window
        self._result = None

    def __str__(self) -> str:
        return f'{self._type.name} {self._status.name} ply={self.ply} pos={self.pos} window={self.window} result={self.result}'

    @property
    def is_pv_node(self) -> bool:
        return self._type == NodeType.PV
    
    @property
    def is_all_node(self) -> bool:
        return self._type == NodeType.All
    
    @property
    def is_cut_node(self) -> bool:
        return self._type == NodeType.Cut

    def serial_nodes(self):
        if self._type == NodeType.PV:
            return 1
        if self._type == NodeType.All:
            return 0
        if self._type == NodeType.Cut:
            return 2
    
    @property
    def is_unsolved(self) -> bool:
        return self._status == NodeStatus.Unsolved
    
    @property
    def is_taken(self) -> bool:
        return self._status == NodeStatus.Taken
    
    @property
    def is_solved(self) -> bool:
        return self._status == NodeStatus.Solved
    
    def update_status(self):
        "update status from children"
        serial_nodes = self.serial_nodes()
        serial_children = self.children[:serial_nodes]
        parallel_children = self.children[serial_nodes:]

        if any(c.is_taken for c in serial_children):
            self.status = NodeStatus.Taken
        elif all(c.is_solved for c in serial_children):
            if any(c.is_unsolved for c in parallel_children):
                self.status = NodeStatus.Unsolved
            elif all(c.is_solved for c in parallel_children):
                self.status = NodeStatus.Solved
                self.children.clear()
            else:
                self.status = NodeStatus.Taken
        else:
            self.status = NodeStatus.Unsolved

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status: NodeStatus):
        self._status, status = status, self._status
        if self._status != status and not self.is_root:
            self.parent.update_status()

    def improve_window_lower(self, value):
        if value > self.window:
            self.result = value
        elif value > self.window.lower:
            self.window.lower = value
            for child in self.children:
                child.improve_window_upper(-value)

    def improve_window_upper(self, value):
        if value < self.window:
            self.result = value
        elif value < self.window.upper:
            self.window.upper = value
            for child in self.children:
                child.improve_window_lower(-value)
                
    def update_result(self):
        "update result from children"
        old_lower = self.window.lower
        best_score = None
        all_solved = True
        for child in self.children:
            if child.is_solved:
                score = -child.result
                if score > self.window:
                    self._result = score
                best_score = max(best_score or score, score)
                self.window.lower = max(self.window.lower, score)
            else:
                all_solved = False

        if all_solved:
            self._result = best_score
        elif self.window.lower > old_lower:
            for child in self.children:
                if child.is_unsolved:
                    child.improve_window_upper(-self.window.lower)
                    
    @property
    def result(self):
        return self._result
    
    @result.setter
    def result(self, result):
        self._result = result
        self.status = NodeStatus.Solved
        if not self.is_root:
            self.parent.update_result()
            

def expand(node: SearchNode, move_sorter, play):
    for i, move in enumerate(move_sorter(node.pos)):
        # child_type
        if node.is_pv_node:
            if i == 0:
                child_type = NodeType.PV
            else:
                child_type = NodeType.Cut
        elif node.is_all_node:
            child_type = NodeType.Cut
        elif node.is_cut_node:
            child_type = NodeType.All
            
        # child_ply
        if move is None:
            child_ply = node.ply
        else:
            child_ply = node.ply - 1
            
        node.append(SearchNode(child_ply, child_type, play(node.pos, move), -node.window))
        

def next_unsolved_leaf_node(node: SearchNode, move_sorter, play):        
    if node.is_taken or node.is_solved:
        return None
        
    # Lazy node expansion
    if node.is_leaf and node.ply > 0:
        expand(node, move_sorter, play)
        
    if node.is_leaf:
        return node
        
    serial_nodes = node.serial_nodes()
    serial_children = node.children[:serial_nodes]
    parallel_children = node.children[serial_nodes:]
    for child in serial_children:
        if not child.is_solved:
            return next_unsolved_leaf_node(child, move_sorter, play)
    for child in parallel_children:
        next_leaf_node = next_unsolved_leaf_node(child, move_sorter, play)
        if next_leaf_node:
            return next_leaf_node
    
    raise RuntimeError("Node is unsolved but had no unsolved children.")


class ParallelTree:
    def __init__(self, ply, pos, window: OpenInterval, move_sorter, play) -> None:
        self.root = SearchNode(ply, NodeType.PV, pos, window)
        self.move_sorter = move_sorter
        self.play = play
        self._lock = threading.Lock()

    def __str__(self) -> str:
        s: str = ''
        indent = self.root.ply
        def append(node):
            nonlocal s, indent
            s += ' ' * (indent - node.ply) + str(node) + '\n'
        traverse_depth_first(self.root, append, lambda *args: None)
        return s

    @property    
    def is_solved(self) -> bool:
        return self.root.is_solved
    
    @property
    def result(self):
        return self.root.result

    def get_task(self):
        with self._lock:
            node = next_unsolved_leaf_node(self.root, self.move_sorter, self.play)
            if node is not None:
                node.status = NodeStatus.Taken
            return node
    
    def get_tasks(self):
        nodes = []
        while True:
            node = self.get_task()
            if node is None:
                return nodes
            nodes.append(node)

    def report(self, node: SearchNode, result):
        with self._lock:
            node.result = result
        
    
class DynamicTreeSearch:
    def __init__(self, dynamic_tree_depth: int, search, move_sorter) -> None:
        self.ply = dynamic_tree_depth
        self.search = search
        self.move_sorter = move_sorter
        
    def eval(self, pos, window: OpenInterval):
        tree = ParallelTree(self.ply, pos, window, self.move_sorter)
        new_report = threading.Condition()
        
        def work_on_tree():
            nonlocal self, tree, new_report
            while not tree.is_solved:
                node = tree.get_task()
                if node is None:
                    new_report.wait()
                    continue
                result = self.search.eval(node.pos, node.window)
                tree.report(node, result)
                new_report.notify_all()
        
        cpu_count = multiprocessing.cpu_count()
        with multiprocessing.Pool(cpu_count) as pool:
            pool.map(work_on_tree, range(cpu_count))
                
        return tree.result