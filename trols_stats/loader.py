import trols_stats.model
import trols_stats.model.entities
import trols_stats.model.aggregates

from logga.log import log

__all__ = ['Loader']


class Loader(object):
    """
    ..attribute:: games_cache
        list of :class:`trols_stats.model.aggregrates.Games` objects

    ..attribute:: players_cache
        list of :class:`trols_stats.model.entities.Player` objects

    """
    def __init__(self):
        self._players_cache = []
        self._games_cache = []

    @property
    def players_cache(self):
        return self._players_cache

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
            del self._players_cache[:]
            self._players_cache = []

        player = None
        for cache in self.players_cache:
            if cmp(cache, player_details):
                log.debug('Player cache hit "%s"' %
                          player_details.get('name'))
                player = cache
                break

        if player is None:
            log.debug('Adding "%s" to player cache' %
                      player_details.get('name'))
            player = trols_stats.model.entities.Player(**player_details)
            self._players_cache.append(player)

        return player

    @property
    def games_cache(self):
        return self._games_cache

    def set_games_cache(self, game_details):
        """Add *game_details* to the cache or return the existing
        :class:`trols_stats.model.Game` object.

        **Args:**
            *game_details*: dictionary of player details in the form::

        **Return:**
            :class:`trols_stats.model.Game` object corresponding to
            *game_details*

        """
        if game_details is None:
            del self._games_cache[:]
            self._games_cache = []

        game = trols_stats.model.Game(**game_details)
        self._game_cache.append(game)

        return game
