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
        log.debug('Name: %s', name)

        def player_team(match):
            return {
                'name': match.get('player').get('name'),
                'team': match.get('player').get('team'),
                'section': match.get('fixture').get('section')
            }

        def player_match(match, name=name):
            return match.get('player').get('name') == name

        db = self.db.connection['trols']

        matched = []
        if name is not None:
            matched = [player_team(x) for x in db if player_match(x)]
        else:
            matched = [player_team(x) for x in db]

        # Uniquefy the dictionaries.
        players = [dict(t) for t in set([tuple(d.items()) for d in matched])]

        return players
