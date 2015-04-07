import trols_stats.model

__all__ = ['Player']


class Player(trols_stats.model.Base):
    """
    .. attribute:: name

    """
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __init__(self, uid=None, name=None):
        super(Player, self).__init__(uid=uid)

        self.__name = name

    def __call__(self):
        return {
            'uid': self.uid,
            'name': self.name,
        }
