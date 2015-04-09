import trols_stats.model

__all__ = ['Player']


class Player(trols_stats.model.Base):
    """
    .. attribute:: name

    .. attribute:: team

    """
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def team(self):
        return self.__team

    @team.setter
    def team(self, value):
        self.__team = value

    def __init__(self, uid=None, name=None, team=None):
        super(Player, self).__init__(uid=uid)

        self.__name = name
        self.__team = team

    def __call__(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'team': self.team,
        }

    def __eq__(self, other):
        is_same = False

        if isinstance(other, dict):
            player = {'name': self.name, 'team': self.team}
            is_same = (cmp(player, other) == 0)
        else:
            is_same = self.__dict__ == other.__dict__

        return is_same
