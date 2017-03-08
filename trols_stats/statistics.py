"""class:`trols_stats.Statistics`.

Data structure managing match statistics.

"""
__all__ = ['Statistics']


class Statistics(object):
    """
        ..attribute:: score_for

        ..attribute:: score_against

        ..attribute:: games_played

        ..attribute:: games_won

        ..attribute:: games_lost

    """
    @property
    def score_for(self):
        return self.__score_for

    @score_for.setter
    def score_for(self, value):
        self.__score_for = value

    @property
    def score_against(self):
        return self.__score_against

    @score_against.setter
    def score_against(self, value):
        self.__score_against = value

    @property
    def games_played(self):
        return self.__games_played

    @games_played.setter
    def games_played(self, value):
        self.__games_played = value

    @property
    def games_won(self):
        return self.__games_won

    @games_won.setter
    def games_won(self, value):
        self.__games_won = value

    @property
    def games_lost(self):
        return self.__games_lost

    @games_lost.setter
    def games_lost(self, value):
        self.__games_lost = value

    def __init__(self):
        self.__score_for = 0
        self.__score_against = 0
        self.__games_played = 0
        self.__games_won = 0
        self.__games_lost = 0

    def __call__(self):
        percent = 0.0
        if self.score_against > 0:
            percent = float(self.score_for) / float(self.score_against) * 100

        return {
            'games_lost': self.games_lost,
            'games_played': self.games_played,
            'games_won': self.games_won,
            'score_against': self.score_against,
            'score_for': self.score_for,
            'percentage': percent
        }

    def aggregate(self, game):
        """Take a :class:`trols_stats.model.aggregate.Game` instance
        and add to the statistics.

        """
        self.games_played += 1

        self.score_for += game.score_for
        self.score_against += game.score_against

        if game.score_for == 6:
            self.games_won += 1
        if game.score_against == 6:
            self.games_lost += 1
