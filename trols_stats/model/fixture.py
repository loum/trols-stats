__all__ = ['Fixture']


class Fixture(object):
    """
    .. attribute::_competition

    """
    _competition = None

    @property
    def competition(self):
        return self._competition

    @competition.setter
    def competition(self, value):
        self._competition = value

    def __init__(self, competition=None):
        if competition is not None:
            self._competition = competition
