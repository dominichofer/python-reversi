class Score(int):

    def __str__(self):
        return f'{self:+03}'


undefined_score: Score = +70
inf_score: Score = +65
