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
    def event(self):
        return self.__event

    @event.setter
    def event(self, value):
        self.__event = value

    def __init__(self, db, event='singles'):
        self.__db = db
        self.__event = event

    def get_players(self,
                    names=None,
                    competition=None,
                    team=None,
                    section=None):
        """Get all players from cache.

        **Args:**
            *names*: list of name to filter DB against

        **Returns:**
            list of simplified player token IDs in the form::

            [
                'Isabella Markovski|Watsonia Red|14',
                ...
            ]

        """
        def cmp_name(name, token):
            return  name.lower() in x.split('|')[0].lower()

        matched = self.db.keys()
        if names is not None:
            matched = [x for x in matched for n in names if cmp_name(n, x)]
            seen = set()
            seen_add = seen.add
            matched = [x for x in matched if not (x in seen or seen_add(x))]

        if team is not None:
            matched = [x for x in matched if x.split('|')[1] == team]

        if section is not None:
            matched = [x for x in matched if x.split('|')[2] == str(section)]

        if competition is not None:
            matched = [x for x in matched if x.split('|')[3] == competition]

        return matched

    def get_player_fixtures(self, name):
        """Search for all fixtures where player *name* participated.

        *Args:*
            *name*: name to filter DB against

        *Returns*: list of all :class:`trols_stats.model.aggregate.Game`
        objects that *name* was involved in

        """
        log.info('Extracting fixtures for player "%s"', name)

        players = [k for k in self.db.keys() if k.split('|')[0] == name]
        fixtures = []
        for player in players:
            fixtures.extend(self.db.get(player))

        return fixtures

    def get_player_singles(self, name):
        """Return list of singles games from all fixtures where player
        *name* participated.

        *Args:*
            *name*: name to filter DB against

        *Returns*: dict of all singles
        :class:`trols_stats.model.aggregate.Game`
        objects that *name* was involved in.  Key is the
        :meth:`trols_stats.model.aggregate.Game.get_player_id` `token`.

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

    def get_player_stats(self,
                         names=None,
                         competition=None,
                         team=None,
                         section=None):
        """Calculates and returns match stats from all fixtures for all
        or nominated players.

        *Args:*
            *names*: list of names to filter DB against

        *Returns*:

        """
        log.info('Generating match stats for player "%s"', names)

        stats = {}
        players = self.get_players(names, competition, team, section)
        for player in players:
            statistics = trols_stats.Statistics(self.event)

            games = self.db.get(player)
            if games is not None:
                for game in games:
                    if ((game.is_singles() and self.event == 'singles')
                            or (game.is_doubles() and self.event == 'doubles')):
                        statistics.aggregate(game)

                stats[player] = statistics()

        return stats

    def sort_stats(self,
                   statistics,
                   key='score_for',
                   reverse=False,
                   limit=None):
        """Manipulate player *name* stats.

        **Args:**
            *key*: as the sort criteria

            *reverse*: if ``True``, will reverse the sort order from lowest
            to highest

        """
        def qualified(statistic):
            is_qualified = False

            games_played = statistic[1].get(self.event).get('games_played')
            if games_played is not None and games_played > 3:
                is_qualified = True

            return is_qualified

        sort_stats = sorted(statistics.iteritems(),
                            key=lambda x: x[1][self.event][key],
                            reverse=reverse)

        if limit is not None:
            sort_stats = [x for x in sort_stats if qualified(x)][:limit]

        return sort_stats
