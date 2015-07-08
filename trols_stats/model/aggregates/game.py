import trols_stats.model
import trols_stats.model.entities as entities

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
        self.__fixture = Game.set_fixture(value)

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        self.__player = Game.set_player(value)

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
    def opposition(self, values):
        self.__opposition = Game.set_opposition(values)

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

        self.__fixture = Game.set_fixture(fixture)
        self.__player = Game.set_player(player)
        self.__team_mate = Game.set_player(team_mate)
        self.__opposition = Game.set_opposition(opposition)
        self.__score_for = score_for
        self.__score_against = score_against

    def __call__(self):
        # Cater for singles where player 2 is None.
        opposition = [self.opposition[0]()]
        if len(self.opposition) == 2 and self.opposition[1] is not None:
            opposition.append(self.opposition[1]())

        game = {
            'uid': self.uid,
            'fixture': self.__fixture(),
            'player': self.__player(),
            'opposition': opposition,
            'score_for': self.score_for,
            'score_against': self.score_against,
        }

        if self.team_mate.name is not None:
            game['team_mate'] = self.__team_mate()

        return game

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        player = {
            'name': self.player.name,
            'section': self.fixture.section,
            'team': self.player.team,
        }
        return player == other

    def player_id(self):
        """Return a dictionary structure that attempts to uniquely
        identify a player.

        """
        return {
            'name': self.player.name,
            'team': self.player.team,
            'section': self.fixture.section,
            'token': '{}|{}|{}'.format(self.player.name,
                                       self.player.team,
                                       self.fixture.section)
        }

    def is_singles(self):
        """Helper method that checks if this game aggregate is
        a singles fixture.

        """
        return (self.player.name is not None
                and self.team_mate.name is None)

    def is_doubles(self):
        """Helper method that checks if this game aggregate is
        a doubles fixture.

        """
        return (self.player.name is not None
                and self.team_mate.name is not None)

    @staticmethod
    def set_opposition(data):
        """Build an opposition players data structure.

        **Args:**
            *data*: Either ``None``, a tuple of
            :class:`trols_stats.model.entities.Player` items or
            dictionary of values that feed into the
            :class:`trols_stats.model.entities.Player` initialiser::

            (
                {
                    'name': 'Isabella Markovski',
                    'team': 'Watsonia',
                },
                ...
            )

        **Returns:** tuple of :class:`trols_stats.model.entities.Player`

        """
        if data is None:
            players = tuple()
        elif all(isinstance(oppn, dict) for oppn in data):
            players = tuple([entities.Player(**oppn) for oppn in data])
        elif all(isinstance(oppn, entities.Player) for oppn in data):
            players = data
        elif isinstance(data[0], entities.Player):
            players = (data[0], None)
        elif isinstance(data[0], dict):
            players = (entities.Player(**data[0]), None)

        return players

    @staticmethod
    def set_player(data):
        """Build a player data structure.

        **Args:**
            *data*: Either ``None``, a tuple of
            :class:`trols_stats.model.entities.Player` items or
            dictionary of values that feed into the
            :class:`trols_stats.model.entities.Player` initialiser::

            (
                {
                    'name': 'Isabella Markovski',
                    'team': 'Watsonia',
                },
            )

        **Returns:** :class:`trols_stats.model.entities.Player` instance

        """
        if data is None:
            player = entities.Player()
        elif isinstance(data, dict):
            player = entities.Player(**data)
        elif isinstance(data, entities.Player):
            player = data

        return player

    @staticmethod
    def set_fixture(data):
        """Build a :class:`trols_stats.model.entities.Fixture` from *data*.

        **Args:**
            *data*: Either ``None``,
            a :class:`trols_stats.model.entities.Fixture` or a
            dictionary of values that feed into the
            :class:`trols_stats.model.entities.Fixture` initialiser::

            (
                {
                    'away_team': 'St Marys',
                    'competition': 'girls',
                    'date': '28 Feb 15',
                    'home_team': 'Watsonia Red',
                    'match_round': 5,
                    'section': 14,
                    'uid': None
                }
            }

        **Returns:** :class:`trols_stats.model.entities.Fixture` instance

        """
        if data is None:
            fixture = entities.Fixture()
        elif isinstance(data, dict):
            fixture = entities.Fixture(**data)
        elif isinstance(data, entities.Fixture):
            fixture = data

        return fixture
