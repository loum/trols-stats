import trols_stats
from logga.log import log


class Reporter(object):
    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value):
        self.__db = value

    @property
    def statistics_cache(self):
        return self.__statistics_cache

    def __init__(self, shelve=None):
        self.__db = trols_stats.DBSession(shelve=shelve)
        self.__db.connect()
        self.__statistics_cache = {}

    def get_players(self, name=None):
        """Get all players from cache.

        **Args:**
            *name*: name to filter DB against

        **Returns:**
            list of simplified player dictionaries if the form::

            {
                'name': 'Isabella Markovski',
                'section': 14,
                'team': u'Watsonia Red'
                'token': 'Isabella Markovski|Watsonia Red|14'
            }

        """
        log.info('Extracting all instances for player: "%s"', name)

        db = self.db.connection['trols']

        matched = []
        if name is not None:
            matched = [x for x in db.keys() if x.split('|')[0] == name]
        else:
            matched = [x for x in db.keys()]

        return matched

    def get_player_fixtures(self, name):
        """Search for all fixtures where player *name* participated.

        *Args:*
            *name*: name to filter DB against

        *Returns*: list of all :class:`trols_stats.model.aggregate.Game`
        objects that *name* was involved in

        """
        log.info('Extracting fixtures for player "%s"', name)

        db = self.db.connection['trols']
        # player_instances = self.get_players(name)
        # fixtures = [x for x in db if x.player_id() in player_instances]

        #log.info('Total fixures found with player "%s": %d',
        #         name, len(fixtures))

        players = [k for k in db.keys() if k.split('|')[0] == name]
        fixtures = []
        for player in players:
            fixtures.extend(db.get(player))

        return fixtures

    def get_player_singles(self, name):
        """Return list of singles games from all fixtures where player
        *name* participated.

        *Args:*
            *name*: name to filter DB against

        *Returns*: list of all singels
        :class:`trols_stats.model.aggregate.Game`
        objects that *name* was involved in

        """
        log.info('Extracting singles games for player "%s"', name)

        fixtures = self.get_player_fixtures(name)

        singles_games = [x for x in fixtures if x.is_singles()]

        log.info('Total singles games found with player "%s": %d',
                 name, len(singles_games))

        return singles_games

    def get_player_doubles(self, name):
        """Return list of doubles games from all fixtures where player
        *name* participated.

        *Args:*
            *name*: name to filter DB against

        *Returns*: list of all doubles
        :class:`trols_stats.model.aggregate.Game`
        objects that *name* was involved in

        """
        log.info('Extracting doubles games for player "%s"', name)

        fixtures = self.get_player_fixtures(name)

        doubles_games = [x for x in fixtures if x.is_doubles()]

        log.info('Total doubles games found with player "%s": %d',
                 name, len(doubles_games))

        return doubles_games

    def get_player_stats(self, name):
        """Calculates and returns match stats from all fixtures for all
        or nominated players.

        *Args:*
            *name*: name to filter DB against

        *Returns*:

        """
        log.info('Generating match stats for player "%s"', name)

        db = self.db.connection['trols']
        stats = {}
        players = self.get_players(name)
        player_count = len(players)
        counter = 1
        for player in players:
            singles_stats = trols_stats.Statistics('singles')
            doubles_stats = trols_stats.Statistics('doubles')

            games = db.get(player)
            if games is None:
                games = []
            for game in games:
                if game.is_singles():
                    singles_stats.aggregate(game)
                else:
                    doubles_stats.aggregate(game)

            stats[player] = {
                'singles': singles_stats().get('singles'),
                'doubles': doubles_stats().get('doubles'),
            }
            log.debug('Statistics generated for "%s": %d of %d',
                      player, counter, player_count)
            counter += 1

        return stats
