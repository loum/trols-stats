import trols_stats.model
import trols_stats.model.entities
import trols_stats.model.aggregates

from logga.log import log

__all__ = ['Loader']


class Loader(object):
    """
    ..attribute:: players

    ..attribute:: games_cache
        list of :class:`trols_stats.model.aggregrates.Games` objects

    ..attribute:: players_cache
        list of :class:`trols_stats.model.entities.Player` objects

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
            self.__players = {}
        else:
            self.__players = players

        if teams is None:
            self.__teams = {}
        else:
            self.__teams = teams

        if fixture is None:
            self.__fixture = {}
        else:
            self.fixture = fixture

        self.__players_cache = []
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
        if player_details is None:
            del self.__players_cache[:]
            self.__players_cache = []

        player = None
        for cache in self.__players_cache:
            if cache == player_details:
                log.debug('Player cache hit "%s"' %
                          player_details.get('name'))
                player = cache
                break

        if player is None:
            log.debug('Adding "%s" to player cache' %
                      player_details.get('name'))
            player = trols_stats.model.entities.Player(**player_details)
            self.__players_cache.append(player)

        return player

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
        if game_details is None:
            del self.__games_cache[:]
            self.__games_cache = []

        game = trols_stats.model.aggregates.Game(**game_details)
        self.__games_cache.append(game)

        return game

    def build_game_aggregate(self, stats):
        """Build the :class:`trols_stats.model.aggregates.Game` aggregate
        objects.  All new aggregate object will be placed on the
        :attr:`games_cache` list attribute.

        **Args:**
            *stats*: the match statistics in the form::

                {1: [
                    {
                        'opposition': (5, 6),
                        'score_against': 6,
                        'score_for': 3,
                        'team_mate': 2
                    }
                ]}

        """
        for code, games in stats.iteritems():
            player_obj = self.set_players_cache(self.get_player(code))

            for game in games:
                # Opposition players.
                opposition = game.get('opposition')
                opposition_data_1 = self.get_player(opposition[0])
                opposition_obj_1 = self.set_players_cache(opposition_data_1)
                opposition_data_2 = self.get_player(opposition[1])
                opposition_obj_2 = self.set_players_cache(opposition_data_2)

                # Team mate.
                team_mate = game.get('team_mate')
                team_mate_data = self.get_player(team_mate)
                team_mate_obj = self.set_players_cache(team_mate_data)

                # Score against.
                score_against = game.get('score_against')

                # Score for.
                score_for = game.get('score_for')

                game = trols_stats.model.aggregates.Game()
                game.score_for = score_for
                game.score_against = score_against

                game_data = {'fixture': self.fixture,
                             'player': player_obj,
                             'team_mate': team_mate_obj,
                             'opposition': (opposition_obj_1,
                                            opposition_obj_2),
                             'score_for': score_for,
                             'score_against': score_against}

                self.set_games_cache(game_data)

    def get_player(self, code):
        name = self.players.get(code)
        team = self.teams.get('away' if code / 4 else 'home')

        return {'name': name, 'team': team}
