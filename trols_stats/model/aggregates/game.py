import trols_stats.model
import trols_stats.model.entities as entities
from logga import log

__all__ = ['Game']


class Game(trols_stats.model.Base):
    """
    .. attribute:: fixture

    .. attribute:: player

    .. attribute:: team_mate

    .. attribute:: opposition

    .. attribute:: score_for

    .. attribute:: score_against

    .. attribute:: player_won

    """
    @property
    def fixture_round(self):
        return self.__fixture.match_round

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

    @property
    def player_won(self):
        return self.__player_won

    @player_won.setter
    def player_won(self, value):
        self.__player_won = value

    def __init__(self,
                 fixture=None,
                 player=None,
                 team_mate=None,
                 opposition=None,
                 score_for=None,
                 score_against=None):

        self.__fixture = Game.set_fixture(fixture)
        self.__player = Game.set_player(player)
        self.__team_mate = Game.set_player(team_mate)
        self.__opposition = Game.set_opposition(opposition)
        self.__score_for = score_for
        self.__score_against = score_against
        self.__player_won = None

        log.debug('SF|SA: %s|%s', self.__score_for, self.__score_against)
        if (self.__score_for is not None
                and self.__score_against is not None):
            if self.__score_for in [6, 8] and self.__score_against != 8:
                log.debug('Player Won')
                self.__player_won = True
            if self.__score_against in [6, 8] and self.__score_for != 8:
                log.debug('Player Lost')
                self.__player_won = False

    def __call__(self):
        # Cater for singles where player 2 is None.
        opposition = [self.opposition[0]()]
        if len(self.opposition) == 2 and self.opposition[1] is not None:
            opposition.append(self.opposition[1]())

        game = {
            'fixture': self.__fixture(),
            'player': self.__player(),
            'opposition': opposition,
            'score_for': self.score_for,
            'score_against': self.score_against,
            'player_won': self.player_won,
        }

        if self.team_mate.name is not None:
            game['team_mate'] = self.__team_mate()

        return game

    def compact_match(self):
        """Returns a simple, compact representation of the object instance.

        """
        # Cater for singles where player 2 is None.
        opposition = [self.opposition[0].name]
        if len(self.opposition) == 2 and self.opposition[1] is not None:
            opposition.append(self.opposition[1].name)

        fixture = {
            'match_type': 'singles' if self.is_singles() else 'doubles',
            'match_round': self.fixture.match_round,
            'date_played': self.fixture.comvert_match_date(),
            'home_team': self.fixture.home_team,
            'away_team': self.fixture.away_team,
            'player': self.player.name,
            'player_team': self.player.team,
            'opposition': opposition,
            'score_for': self.score_for,
            'score_against': self.score_against,
            'player_won': self.player_won,
        }

        if self.is_doubles():
            fixture['team_mate'] = self.team_mate.name

        return fixture

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
        args = (
            self.player.name,
            self.player.team,
            self.fixture.section,
            self.fixture.competition_type,
            self.fixture.competition
        )

        return {
            'name': self.player.name,
            'team': self.player.team,
            'section': self.fixture.section,
            'competition_type': self.fixture.competition_type,
            'competition': self.fixture.competition,
            'token': '{}~{}~{}~{}~{}'.format(*args)
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
