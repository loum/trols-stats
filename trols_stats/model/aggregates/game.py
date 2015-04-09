import trols_stats.model
import trols_stats.model.entities

__all__ = ['Game']


class Game(trols_stats.model.Base):
    """
    .. attribute:: fixture

    .. attribute:: player

    .. attribute:: team_mate

    .. attribute:: opposition

    .. attribute:: score_for

    .. attribute:: score_against

    """
    @property
    def fixture(self):
        return self.__fixture

    @fixture.setter
    def fixture(self, value):
        self.__fixture = value

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        self.__player = value

    @property
    def team_mate(self):
        return self.__team_mate

    @team_mate.setter
    def team_mate(self, value):
        self.__team_mate = value

    @property
    def opposition(self):
        return self.__opposition

    @opposition.setter
    def opposition(self, value):
        self.__opposition = value

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

    def __init__(self,
                 uid=None,
                 fixture=None,
                 player=None,
                 team_mate=None,
                 opposition=None,
                 score_for=None,
                 score_against=None):
        super(Game, self).__init__(uid=uid)

        if fixture is None:
            self.__fixture = trols_stats.model.entities.Fixture()
        else:
            self.__fixture = fixture

        if player is None:
            self.__player = trols_stats.model.entities.Player()
        else:
            self.__player = player

        if team_mate is None:
            self.__team_mate = trols_stats.model.entities.Player()
        else:
            self.__team_mate = team_mate

        if opposition is None:
            self.__opposition = (trols_stats.model.entities.Player(),
                                 trols_stats.model.entities.Player())
        else:
            self.__opposition = opposition

        self.__score_for = score_for
        self.__score_against = score_against

    def __call__(self):
        return {
            'uid': self.uid,
            'fixture': self.fixture(),
            'player': self.player(),
            'opposition': [self.opposition[0](),
                           self.opposition[1]()],
            'team_mate': self.team_mate(),
            'score_for': self.score_for,
            'score_against': self.score_against,
        }

    def __str__(self):
        return str(self.__dict__)
