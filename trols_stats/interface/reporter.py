import trols_stats
from logga.log import log


class Reporter(object):
    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value):
        self.__db = value

    def __init__(self, shelve=None):
        self.__db = trols_stats.DBSession(shelve=shelve)
        self.__db.connect()

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
            }

        """
        log.info('Extracting all instances for player: "%s"', name)

        def player_compare(game, name=name):
            return game.player.name == name

        db = self.db.connection['trols']

        matched = []
        if name is not None:
            matched = [x.player_id() for x in db if player_compare(x)]
        else:
            matched = [x.player_id() for x in db]

        # Unique-ify the matched dictionaries.
        uniq = [dict(t) for t in set([tuple(d.items()) for d in matched])]

        return uniq

    def get_player_fixtures(self, name):
        """Search for all of fixtures where player *name* participated.

        *Args:*
            *name*: name to filter DB against

        *Returns*: list of all :class:`trols_stats.model.aggregate.Game`
        objects that *name* was involved in

        """
        log.info('Extracting fixtures for player "%s"', name)

        db = self.db.connection['trols']
        player_instances = self.get_players(name)
        fixtures = [x for x in db if x.player_id() in player_instances]

        log.info('Total fixures found with player "%s": %d',
                 name, len(fixtures))

        return fixtures
