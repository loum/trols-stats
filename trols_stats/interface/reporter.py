import trols_stats
from logga.log import log


class Reporter(object):
    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value):
        self.__db = value

    def __init__(self, db):
        self.__db = db

    def get_players(self,
                    names=None,
                    competition=None,
                    competition_type=None,
                    team=None,
                    section=None):
        """Get all players from cache.

        **Args:**
            *names*: list of name to filter DB against

        **Returns:**
            list of simplified player token IDs in the form::

            [
                'Isabella Markovski~Watsonia Red~14~girls~saturday_...',
                ...
            ]

        """
        def cmp_name(name, token):
            return  name.lower() in token.split('~')[0].lower()

        def cmp_team(team, token):
            return token.split('~')[1] == team

        def cmp_section(section, token):
            return token.split('~')[2] == str(section)

        def cmp_comp_type(competition_type, token):
            return token.split('~')[3] == competition_type

        def cmp_comp(competition, token):
            return token.split('~')[4] == str(competition)

        matched = self.db.keys()
        if names is not None:
            matched = [x for x in matched for n in names if cmp_name(n, x)]
            seen = set()
            seen_add = seen.add
            matched = [x for x in matched if not (x in seen or seen_add(x))]

        if team is not None:
            matched = [x for x in matched if cmp_team(team, x)]

        if section is not None:
            matched = [x for x in matched if cmp_section(section, x)]

        if competition_type is not None:
            matched = [x for x in matched if cmp_comp_type(competition_type, x)]

        if competition is not None:
            matched = [x for x in matched if cmp_comp(competition, x)]

        return sorted(matched)

    def get_player_fixtures(self, player_token):
        """Search for all fixtures where player *name* participated.

        *Args:*
            *player_token*: player token ID to filter DB against.  For
            example::

                Joel Markovski~Watsonia~20~boys~saturday_am_autum_2015

        *Returns*: list of all :class:`trols_stats.model.aggregate.Game`
        objects that *name* was involved in

        """
        game_aggregates = self.db.get(player_token)
        if game_aggregates is None:
            game_aggregates = []

        return game_aggregates

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

    def get_player_stats(self, player_tokens=None):
        """Calculates and returns match stats from all fixtures for all
        or nominated players.

        *Args:*
            *player_tokens*: list of player token ID to filter DB against.
            For example::

                Joel Markovski~Watsonia~20~boys~saturday_am_autum_2015

        *Returns*:

        """
        if player_tokens is None:
            player_tokens = self.db.keys()

        stats = {}
        for player_token in player_tokens:
            singles_stats = trols_stats.Statistics()
            doubles_stats = trols_stats.Statistics()

            game_aggregates = self.get_player_fixtures(player_token)
            for game in game_aggregates:
                if game.is_singles():
                    singles_stats.aggregate(game)
                elif game.is_doubles():
                    doubles_stats.aggregate(game)

            (name, team, section, comp_type, comp) = player_token.split('~')
            stats[player_token] = {
                'name': name,
                'team': team,
                'section': section,
                'comp_type': comp_type,
                'comp': comp,
                'singles': singles_stats(),
                'doubles': doubles_stats(),
            }

        return stats

    def sort_stats(self,
                   statistics,
                   event='singles',
                   key='score_for',
                   reverse=False,
                   limit=None):
        """Manipulate player *name* stats.

        **Args:**
            *statistics*:

        **Kwargs:**
            *key*: as the sort criteria

            *reverse*: if ``True``, will reverse the sort order from lowest
            to highest

        """
        def qualified(statistic):
            is_qualified = False

            games_played = statistic[1].get(event).get('games_played')
            if games_played is not None and games_played > 3:
                is_qualified = True

            return is_qualified

        sort_stats = sorted(statistics.iteritems(),
                            key=lambda x: x[1][event][key],
                            reverse=reverse)

        if limit is not None:
            sort_stats = [x for x in sort_stats if qualified(x)][:limit]

        return sort_stats
