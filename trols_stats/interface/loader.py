import trols_stats

__all__ = ['Loader']


class Loader(object):
    """
    .. attribute:: games

    """
    @property
    def games(self):
        return self.__games

    @games.setter
    def games(self, value):
        self.__games = value

    def __init__(self):
        self.__games = []
