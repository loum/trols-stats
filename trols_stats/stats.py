"""class:`trols_stats.Stats`.

"""
import trols_stats.model
import trols_stats.model.entities
import trols_stats.model.aggregates
from logga import log

__all__ = ['Stats']


class Stats(object):
    """
    ..attribute:: players
        list of tuples that represent the player number in the match
        and the name of the player.  For example::

            [
                (1, 'Mladena Mitic'),
                (2, 'Erica Bramble'),
                (3, 'Indiana Pisasale'),
                (4, 'Sasha Pecanic'),
                (5, 'Shania Peric'),
                (6, 'Maddison Batchelor'),
                (7, 'Kristen Fisher'),
                (8, 'Paris Batchelor')
            ]

       Player numbers 1-4 make up the Home Team.  5-8 are the Away Team

    ..attribute:: teams
        data structure that represents the match Home and Away teams.
        For example::

            {'away_team': 'Eltham', 'home_team': 'Norris Bank'}

        The keys ``away_team`` and ``away_team`` are required

    ..attribute:: fixture
        dict data structure that represents the details of the match.
        For example::

            {
                'competition_type': 'girls',
                'competition': 'saturday_am_autumn_2015',
                'section': 1,
                'date': '21 Feb 15',
                'match_round': 4,
                'home_team': 'Norris Bank',
                'away_team': 'Eltham',
            }

    ..attribute:: games_cache
        list of :class:`trols_stats.model.aggregrates.Games` objects

    ..attribute:: players_cache
        list of :class:`trols_stats.model.entities.Player` objects

    ..attribute:: fixtures_cache
        list of :class:`trols_stats.model.entities.Fixture` objects

    """
    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, value):
        self.__players = value

    @property
    def teams(self):
        return self.__teams

    @teams.setter
    def teams(self, value):
        self.__teams = value

    @property
    def fixture(self):
        return self.__fixture

    @fixture.setter
    def fixture(self, value):
        self.__fixture = trols_stats.model.entities.Fixture(**value)

    def __init__(self, players=None, teams=None, fixture=None):
        if players is None:
            players = {}
        self.__players = players

        if teams is None:
            teams = {}
        self.__teams = teams

        if fixture is None:
            fixture = {}
        self.__fixture = trols_stats.model.entities.Fixture(**fixture)

        self.__players_cache = []
        self.__fixtures_cache = []
        self.__games_cache = []

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def players_cache(self):
        return self.__players_cache

    def set_players_cache(self, player_details):
        """Add *player_details* to the cache or return the existing
        :class:`trols_stats.model.entities.Player` object.

        **Args:**
            *player_details*: dictionary of player details in the form::

                {'name': '<player_name'>,
                 'team': '<player_team>'}

        **Return:**
            :class:`trols_stats.model.entities.Player` object
            corresponding to *player_details*

        """
        player = None

        if player_details is not None:
            for cache in self.__players_cache:
                if cache == player_details:
                    log.debug('Player cache hit "%s"',
                              player_details.get('name'))
                    player = cache
                    break

            if player is None:
                log.debug('Adding "%s" to player cache',
                          player_details.get('name'))
                player = trols_stats.model.entities.Player(**player_details)
                self.__players_cache.append(player)

        return player

    @property
    def fixtures_cache(self):
        return self.__fixtures_cache

    def set_fixtures_cache(self, fixture_details):
        """Add *fixture_details* to the cache or return the existing
        :class:`trols_stats.model.entities.Fixture` object.

        **Args:**
            *fixture_details*: dictionary of fixture details.  For example::

                {
                    'competition': 'girls',
                    'section': 14,
                    'date': '28 Feb 15',
                    'match_round': 5,
                    'home_team': 'Watsonia Red',
                    'away_team': 'St Marys',
                }

        **Return:**
            :class:`trols_stats.model.entities.Fixture` object
            corresponding to *fixture_details*

        """
        fixture = None
        for cache in self.__fixtures_cache:
            if cache == fixture_details:
                log.debug('Fixture cache hit "%s %s round %s"',
                          fixture_details.get('competition'),
                          fixture_details.get('section'),
                          fixture_details.get('match_round'))
                fixture = cache
                break

        if fixture is None:
            log.debug('Adding "%s %s round %s" to fixture cache',
                      fixture_details.get('competition'),
                      fixture_details.get('section'),
                      fixture_details.get('match_round'))
            fixture = trols_stats.model.entities.Fixture(**fixture_details)
            self.__fixtures_cache.append(fixture)

        return fixture

    @property
    def games_cache(self):
        return self.__games_cache

    def set_games_cache(self, game_details):
        """Add *game_details* to the cache or return the existing
        :class:`trols_stats.model.aggregates.Game` object.

        **Args:**
            *game_details*: dictionary of player details in the form::

        **Return:**
            :class:`trols_stats.model.aggregates.Game` object
            corresponding to *game_details*

        """
        game = trols_stats.model.aggregates.Game(**game_details)
        self.__games_cache.append(game)

        return game

    def build_game_aggregate(self, stats):
        """Build the :class:`trols_stats.model.aggregates.Game` aggregate
        objects.  All new aggregate object will be placed on the
        :attr:`games_cache` list attribute.

        **Args:**
            *stats*: the match statistics in the form::

                {
                    1: [
                        {
                            'opposition': (5, 6),
                            'score_against': 6,
                            'score_for': 3,
                            'team_mate': 2
                        }
                    ]
                }

        """
        for code, games in stats.items():
            player_obj = self.set_players_cache(self.get_player(code))

            for raw_game in games:
                if raw_game is None:
                    log.warn('Incomplete raw game detail: skipping')
                    continue

                # Team mate.
                team_mate = raw_game.get('team_mate')
                team_mate_obj = None
                if team_mate is not None:
                    team_mate_data = self.get_player(team_mate)
                    team_mate_obj = self.set_players_cache(team_mate_data)

                # Score against.
                score_against = raw_game.get('score_against')

                # Score for.
                score_for = raw_game.get('score_for')

                game_data = {
                    'fixture': self.fixture,
                    'player': player_obj,
                    'opposition':
                        self.get_opposition(raw_game.get('opposition')),
                    'score_for': score_for,
                    'score_against': score_against
                }

                if team_mate_obj is not None:
                    game_data['team_mate'] = team_mate_obj

                self.set_games_cache(game_data)

    def get_player(self, code):
        """Return the name and team of player defined by *code*.

        **Args:**
            *code*: integer representing the match player code

        **Returns:**
            player details within a dict structure.  For example::

                {'team': 'Norris Bank', 'name': 'Indiana Pisasale'}

        """
        player = None
        if code is not None:
            name = self.players.get(code)
            index = 'away_team' if int((code - 1) / 4) else 'home_team'
            team = self.teams.get(index)
            player = {'name': name, 'team': team}

            log.debug('Player code "%d" lookup produced "%s"',
                      code, player)

        return player

    def get_opposition(self, opposition_codes):
        """Get the opposition player details.

        **Args:**
            *opposition_codes*: tuple structure that represents
            the player code (1-8) for a particular match.  A singles match
            for example could as::

                (3, None)

            Here, the opposition player code 3 represents home team player 3

        **Returns:**
            Tuple of :class:`trols_stats.model.entities.player.Player` objects

        """
        opposition_data_1 = self.get_player(opposition_codes[0])
        player_1 = self.set_players_cache(opposition_data_1)

        opposition_data_2 = self.get_player(opposition_codes[1])
        player_2 = self.set_players_cache(opposition_data_2)

        return (player_1, player_2)
