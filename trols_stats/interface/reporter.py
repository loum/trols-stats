"""class:`trols_stats.Reporter`

Statistics reporting module.

"""
import re
import collections
import logging

import trols_stats


class Reporter:
    def __init__(self, db):
        self.__db = db()

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value):
        self.__db = value

    def get_players(self,
                    names=None,
                    competition=None,
                    competition_type=None,
                    team=None,
                    section=None):
        """Get all players from cache.

        **Kwargs:**
            *competition*: the competition identifier.  For example::

                'nejta_saturday_am_spring_2015'

            *competition_type*: 'girls' or 'boys'.  (``None`` includes
            both)

            *section*: section level.  (``None`` includes all sections)

        **Returns:**
            list of simplified player token IDs in the form::

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

        return self.player_ids_dict(matched)

    @staticmethod
    def get_competition_details(competition):
        """Ugly, hardwired event/event type lookup based on
        *competition*.

        **Args:**
            *competition*: competition token to use as the mapper trigger

        **Returns:**
            dictionary structure representing the event/event type::

            {
                'event': ['doubles'],
                'event_type': ['mens'],
            }

        """
        comp_details = None

        if re.match('dvta_(tuesday|thursday)_night', competition):
            comp_details = {
                'event': ['doubles'],
                'event_type': ['mens'],
            }
        elif re.match('dvta_thursday_am', competition):
            comp_details = {
                'event': ['doubles'],
                'event_type': ['womens'],
            }
        elif re.match('dvta_friday_night', competition):
            comp_details = {
                'event': ['singles'],
                'event_type': ['mixed'],
            }
        elif re.match('nejta', competition):
            comp_details = {
                'event': ['singles', 'doubles'],
                'event_type': ['girls', 'boys'],
            }

        return comp_details

    def get_competitions(self):
        """Return a list of all competitions represented in the current
        data set.

        **Returns:**
            list of cometitions.  For example::

                [
                    'nejta_saturday_am_autumn_2014',
                    'nejta_saturday_am_autumn_2015',
                    'nejta_saturday_am_spring_2014',
                    'nejta_saturday_am_spring_2015',
                    ...
                ]

        """
        competitions = set(x.split('~')[4] for x in self.db.keys())

        return sorted(competitions)

    def get_teams(self,
                  competition='nejta_saturday_am_spring_2015',
                  competition_type=None,
                  section=None):
        """Filter teams based on *competition*, *competition_type*
        and *section*.

        **Kwargs:**
            *competition*: the TROLS Stats competiton key of the form::

                <association>_<day>_<time_slot>_<season>_<year>

            For example::
                'nejta_saturday_am_spring_2015'

            *competition_type*: one of ``girls``, ``boys`` or ``None``
            for any

            *section*: numeric representation of the team section number

        **Returns:**
            sorted list of team names of the form::

                [
                    'Bundoora',
                    'Eaglemont',
                    'Mill Park',
                    'Rosanna',
                    ...
                ]

        """
        kwargs = {
            'competition': competition,
            'competition_type': competition_type,
            'section': section
        }
        tokens = self.get_players(**kwargs)

        teams = set(x.get('token').split('~')[1] for x in tokens)

        return sorted(teams)

    def get_sections(self,
                     competition='nejta_saturday_am_spring_2015',
                     competition_type=None):
        """Filter sections based on *competition* and *competition_type*.

        **Kwargs:**
            *competition*: the competition code (default
            ``nejta_saturday_am_spring_2015``)

            *competition_type*: either ``boys``, ``girls`` or ``None``

        **Returns:**
            sorted list of integer section numbers

        """
        kwargs = {
            'competition': competition,
            'competition_type': competition_type
        }
        tokens = self.get_players(**kwargs)

        sections = set(x.get('token').split('~')[2] for x in tokens)

        return sorted([int(x) for x in sections])

    def get_player_fixtures(self, player_token):
        """Search for all fixtures where player *name* participated.

        *Args:*
            *player_token*: player token ID to filter DB against.  For
            example::

                Joel Markovski~Watsonia~20~boys~saturday_am_autumn_2015

        *Returns*: list of all :class:`trols_stats.model.aggregate.Game`
        objects that *name* was involved in

        """
        match_aggregates = self.db.get(player_token)
        if match_aggregates is None:
            match_aggregates = []
        else:
            match_aggregates = sorted(match_aggregates,
                                      key=lambda x: x.fixture.match_round_numeric)

        return match_aggregates

    @staticmethod
    def last_fixture_played(games):
        """Sort through the list of *games* and identify the last
        fixture played.

        *Args:*
            *games*: list of :class:`trols_stata.model.aggregates.Games`
            model instances

        *Returns:*
            list of games that were played last

        """
        rounds = [x.fixture.match_round for x in games]

        last_fixture = []
        if rounds:
            if 'Grand Final' in rounds:
                last_round = 'Grand Final'
            elif 'Prelim Final' in rounds:
                last_round = 'Prelim Final'
            elif 'Semi Final' in rounds:
                last_round = 'Semi Final'
            else:
                last_round = rounds[-1]

        last_fixture = [x for x in games if x.fixture.match_round == last_round]

        return last_fixture

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
        logging.info('Extracting singles games for player "%s"', name)

        fixtures = self.get_player_fixtures(name)

        singles_games = [x for x in fixtures if x.is_singles()]

        logging.info('Total singles games found with player "%s": %d', name, len(singles_games))

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
        logging.info('Extracting doubles games for player "%s"', name) 
        fixtures = self.get_player_fixtures(name)

        doubles_games = [x for x in fixtures if x.is_doubles()]

        logging.info('Total doubles games found with player "%s": %d', name, len(doubles_games))

        return doubles_games

    def get_player_stats(self,
                         player_tokens=None,
                         last_fixture=False,
                         event=None):
        """Calculates and returns match stats from all fixtures for all
        or nominated players.

        *Args:*
            *player_tokens*: list of player token ID to filter DB against.
            For example::

                Joel Markovski~Watsonia~20~boys~saturday_am_autumn_2015

        *Kwargs:*
            *last_fixture* boolean flag to indicate if the last fixture
            played with the associated player_token shoule be included

        *Returns*:
            dictionary of player statistics where the key is the
            player token ID and the values take the form::

                {
                    'name': name,
                    'team': team,
                    'section': section,
                    'comp_type': comp_type,
                    'comp': comp,
                    'singles': singles_stats(),
                    'doubles': doubles_stats(),
                    'last_fixture': last_fixture_played(),
                }

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

            stats[player_token] = {
                'singles': singles_stats(),
                'doubles': doubles_stats(),
            }
            player_details = self.player_ids_dict([player_token])
            stats[player_token].update(player_details[0])

            if last_fixture:
                event_aggregates = list(game_aggregates)
                if event is not None and event == 'singles':
                    event_aggregates = self.get_player_singles(player_token)
                elif event is not None and event == 'doubles':
                    event_aggregates = self.get_player_doubles(player_token)

                fixture = self.last_fixture_played(event_aggregates)
                if fixture:
                    fixture = [x() for x in fixture]

                stats[player_token]['last_fixture'] = fixture

        return stats

    @staticmethod
    def sort_stats(statistics,
                   event='singles',
                   key='score_for',
                   reverse=False,
                   limit=None):
        """Sort the given dictionary of :class:`trols_stats.Statistics`
        based on order criteria denoted by *event*, *key* and whether
        the order is *reverse*.

        **Args:**
            *statistics*: as per :meth:`get_player_stats` return value

        **Kwargs:**
            *event*: since the :class:`trols_stats.Statistics` item
            contains both *singles* and *doubles* scores we need to denote
            which event to sort by.  Default is *singles*

            *key*: :class:`trols_stats.Statistics` attribute
            to sort by.  Possible values include *games_won*,
            *games_played*, *percentage*, *score_against*, *games_lost*
            or *score_for*.  Default, *score_for*

            *reverse*: if ``True``, will reverse the sort order from lowest
            to highest

            *limit*: limit the number of :class:`trols_stats.Statistics`
            items to return after sorting.  Setting a *limit* will also
            trigger the qualified metric that will further filter the
            results based on whether the athlete has played more that 3
            matches.

        **Returns:**
            Same as :meth:`get_player_stats`

        """
        def qualified(statistic):
            is_qualified = False

            games_played = statistic[1].get(event).get('games_played')
            if games_played is not None and games_played > 3:
                is_qualified = True

            return is_qualified

        stats = sorted(statistics.items(),
                       key=lambda x: x[1][event][key],
                       reverse=reverse)

        if limit is not None:
            stats = [x for x in stats if qualified(x)][:limit]

        return stats

    @staticmethod
    def rank_stats(statistics, event='singles', key='score_for'):
        """Rank the given *statistics*.

        Adds another key, ``rank`` to the *statistics* structure that
        represents the athlete's rank in the list.

        **Args:**
            *statistics*: as per :meth:`get_player_stats` return value

            *event*: since the :class:`trols_stats.Statistics` item
            contains both *singles* and *doubles* scores we need to denote
            which event to sort by.  Default is *singles*

            *key*: :class:`trols_stats.Statistics` attribute
            to sort by.  Possible values include *games_won*,
            *games_played*, *percentage*, *score_against*, *games_lost*
            or *score_for*.  Default, *score_for*

        """
        last_rank = 1
        last_value = None

        for index, stat in enumerate(statistics, start=1):
            if last_value is None:
                logging.debug('This is the first value')
                last_value = stat[1][event][key]

            if last_value == stat[1][event][key]:
                stat[1]['rank'] = last_rank
            else:
                stat[1]['rank'] = index
                last_rank = index
                last_value = stat[1][event][key]

        return statistics

    def get_player_results_compact(self, player_tokens):
        """Get all singles and doubles results associated with
        *player_token*.

        .. note::

            Fixtures are returned in order of match rounds, "Semi Final", "Prelim Final"
            and then "Grand Final" with singles before doubles events.

        *Args:*
            *player_tokens*: list of player token ID to filter DB against.
            For example::

                Joel Markovski~Watsonia~20~boys~saturday_am_autumn_2015

        *Returns*: dict of all singles in a compact format for
        presentation in web templates.  For example::

            {
                'Isabella Markovski~Watsonia~14~girls~saturday_am_autumn_2015': [
                    {
                        'match_type': 'doubles',
                        'match_round': 5,
                        'date_played':
                            datetime.datetime(2015, 2, 28, 0, 0),
                        'home_team': 'Watsonia Red',
                        'away_team': 'St Marys',
                        'player': 'Madeline Doyle',
                        'opposition': ['Lauren Amsing', 'Mia Bovalino'],
                        'score_for': 3,
                        'score_against': 6,
                        'team_mate': 'Tara Watson',
                        'player_won': False,
                    },
                ],
            }

        """
        results = {}

        for player_token in player_tokens:
            player_matches = self.get_player_fixtures(player_token)

            stash = results[player_token] = {}
            stash['rounds'] = collections.OrderedDict()

            events = ['is_singles', 'is_doubles']
            for event in events:
                for m in [x for x in player_matches if getattr(x, event)()]:
                    if stash['rounds'].get(m.fixture_round) is None:
                        stash['rounds'][m.fixture_round] = []
                    stash['rounds'][m.fixture_round].append(m.compact_match())

        return results

    @staticmethod
    def player_ids_dict(player_ids):
        """Helper method that splits the components of the token index
        from *player_ids* list into separate parts.  For example::

        >>> from trols_munder_ui.utils import player_ids_dict
        >>> token = ('Isabella Markovski~Watsonia~12~girls~saturday_am_spring_2015')
        >>> player_ids_dict([token])
        [{'name': 'Isabella Markovski', 'comp_type': 'girls', 'section': '12',
        'team': 'Watsonia', 'token': 'Isabella Markovski~Watsonia~12~girls~sa
        turday_am_spring_2015', 'comp': 'saturday_am_spring_2015'}]

        """
        def player_id_struct(player_id):
            (name, team, section, comp_type, comp) = player_id.split('~')
            comp_parts = comp.split('_')
            comp_string = '{} {} {} {} {}'.format(comp_parts[0].upper(),
                                                  comp_parts[1].title(),
                                                  comp_parts[2].upper(),
                                                  comp_parts[3].title(),
                                                  comp_parts[4])
            return {
                'name': name,
                'team': team,
                'section': section,
                'comp_type': comp_type,
                'comp': comp,
                'comp_string': comp_string,
                'token': player_id,
            }

        return [player_id_struct(x) for x in player_ids]
