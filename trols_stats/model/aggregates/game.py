import trols_stats.model
import trols_stats.model.entities

__all__ = ['Game']


class Game(trols_stats.model.Base):
    """
    .. attribute:: player

    .. attribute:: fixture

    .. attribute:: team_mate

    .. attribute:: opposition

    .. attribute:: score_for

    .. attribute:: score_against

    """
    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        self.__player = value

    @property
    def fixture(self):
        return self.__fixture

    @fixture.setter
    def fixture(self, value):
        self.__fixture = value

    def __init__(self, uid=None):
        super(Game, self).__init__(uid=uid)

        self.__player = trols_stats.model.entities.Player()
        self.__fixture = trols_stats.model.entities.Fixture()
        self.__team_mate = trols_stats.model.entities.Player()
        self.__opposition = (trols_stats.model.entities.Player(),
                             trols_stats.model.entities.Player())
        self.__score_for = None
        self.__score_against = None

    def __call__(self):
        return {
            'uid': self.uid,
        }
