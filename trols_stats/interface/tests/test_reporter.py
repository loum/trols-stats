"""Unit test cases for the :class:`trols_stats.interface.Reporter` class.

"""
import unittest
import operator
import os
import json

import trols_stats
import trols_stats.interface


def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts=False):
    # If this is a unicode string, return its string representation.
    if isinstance(data, str):
        return data.encode('utf-8')

    # If this is a list of values, return list of byteified values.
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]

    # If this is a dictionary, return dictionary of byteified keys and
    # values but only if we haven't already byteified it.
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True):
                _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }

    # If it's anything else, return it in its original form.
    return data


class TestReporter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.__results_dir = os.path.join('trols_stats',
                                         'interface',
                                         'tests',
                                         'results')

        shelve_dir = os.path.join('trols_stats',
                                  'interface',
                                  'tests',
                                  'files')
        # session = trols_stats.DBSession(shelve=shelve_dir)
        # session.connect()
        # cls.__db = session.connection['trols']
        cls._model = trols_stats.DataModel(shelve=shelve_dir)

    def test_init(self):
        """Initialise an trols_stats.interface.Reporter object.
        """
        reporter = trols_stats.interface.Reporter(db=self._model)
        msg = 'Object is not a trols_stats.interface.Reporter'
        self.assertIsInstance(reporter,
                              trols_stats.interface.Reporter,
                              msg)

    def test_get_players(self):
        """Players lookup.
        """
        # Given a player name
        name = ['Eboni Amos']

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_players(name)

        # then I should get the player profile
        expected = [
            {
                'comp': 'nejta_saturday_am_spring_2015',
                'comp_string': 'NEJTA Saturday AM Spring 2015',
                'comp_type': 'girls',
                'name': 'Eboni Amos',
                'section': '12',
                'team': 'Watsonia',
                'token': 'Eboni Amos~Watsonia~12~girls~'
                         'nejta_saturday_am_spring_2015'
            },
            {
                'comp': 'nejta_saturday_am_autumn_2015',
                'comp_string': 'NEJTA Saturday AM Autumn 2015',
                'comp_type': 'girls',
                'name': 'Eboni Amos',
                'section': '14',
                'team': 'Watsonia Blue',
                'token': 'Eboni Amos~Watsonia Blue~14~girls~'
                         'nejta_saturday_am_autumn_2015'
            },
            {
                'comp': 'nejta_saturday_am_spring_2014',
                'comp_string': 'NEJTA Saturday AM Spring 2014',
                'comp_type': 'girls',
                'name': 'Eboni Amos',
                'section': '15',
                'team': 'Watsonia Red',
                'token': 'Eboni Amos~Watsonia Red~15~girls~'
                         'nejta_saturday_am_spring_2014'
            },
        ]
        msg = 'Player instance mismatch'
        self.assertListEqual(sorted(received,
                                    key=operator.itemgetter('name',
                                                            'section')),
                             expected,
                             msg)

    def test_get_players_lowercase(self):
        """Players lookup: lower case.
        """
        # Given a player name with lower casing
        name = ['eboni amos']

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_players(names=name)

        # then I should get the player profile
        expected = [
            {
                'comp': 'nejta_saturday_am_spring_2015',
                'comp_string': 'NEJTA Saturday AM Spring 2015',
                'comp_type': 'girls',
                'name': 'Eboni Amos',
                'section': '12',
                'team': 'Watsonia',
                'token': 'Eboni Amos~Watsonia~12~girls~'
                         'nejta_saturday_am_spring_2015'
            },
            {
                'comp': 'nejta_saturday_am_autumn_2015',
                'comp_string': 'NEJTA Saturday AM Autumn 2015',
                'comp_type': 'girls',
                'name': 'Eboni Amos',
                'section': '14',
                'team': 'Watsonia Blue',
                'token': 'Eboni Amos~Watsonia Blue~14~girls~'
                         'nejta_saturday_am_autumn_2015'
            },
            {
                'comp': 'nejta_saturday_am_spring_2014',
                'comp_string': 'NEJTA Saturday AM Spring 2014',
                'comp_type': 'girls',
                'name': 'Eboni Amos',
                'section': '15',
                'team': 'Watsonia Red',
                'token': 'Eboni Amos~Watsonia Red~15~girls~'
                         'nejta_saturday_am_spring_2014'
            },
        ]
        msg = 'Player instance mismatch'
        self.assertListEqual(sorted(received,
                                    key=operator.itemgetter('name',
                                                            'section')),
                             expected,
                             msg)

    def test_get_players_lowercase_multiple_part_names(self):
        """Players lookup: lower case.
        """
        # Given a player part names
        names = ['isabella', 'markovski']

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_players(names=names)

        # then I should get the player profile
        msg = 'Players multi part query error'
        self.assertEqual(len(received), 20, msg)

    def test_get_players_team_and_section(self):
        """Players lookup: team and section.
        """
        # Given a team name
        team = 'Watsonia Blue'

        # and a section
        section = 14

        # when I query the players
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = json.dumps(reporter.get_players(team=team,
                                                   section=section))
        received = json_loads_byteified(received)

        # then I should get the player profile
        with open(os.path.join(self.__results_dir,
                               'players_team_and_section.json')) as _fh:
            expected = json_loads_byteified(_fh.read().strip())
        msg = 'Player instance mismatch'
        self.assertListEqual(sorted(received,
                                    key=lambda x: x.get(b'name')),
                             expected,
                             msg)

    def test_get_players_team(self):
        """Players lookup: team.
        """
        # Given a team name
        team = 'Watsonia'

        # when I query the players
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_players(team=team)

        # then I should get the player profile
        msg = 'Player instance (team search) count error'
        self.assertEqual(len(received), 242, msg)

    def test_get_players_name_and_competition(self):
        """Players lookup: name and compeition.
        """
        # Given a player name
        names = ['markovski']

        # and a competition
        competition = 'nejta_saturday_am_spring_2015'

        # when I query the players
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_players(names=names,
                                        competition=competition)

        # then I should get the player profile
        expected = [
            {
                'comp': 'nejta_saturday_am_spring_2015',
                'comp_string': 'NEJTA Saturday AM Spring 2015',
                'comp_type': 'girls',
                'name': 'Isabella Markovski',
                'section': '12',
                'team': 'Watsonia',
                'token': 'Isabella Markovski~Watsonia~12~girls~'
                         'nejta_saturday_am_spring_2015'
            },
            {
                'comp': 'nejta_saturday_am_spring_2015',
                'comp_string': 'NEJTA Saturday AM Spring 2015',
                'comp_type': 'boys',
                'name': 'Joel Markovski',
                'section': '21',
                'team': 'Watsonia',
                'token': 'Joel Markovski~Watsonia~21~boys~'
                         'nejta_saturday_am_spring_2015'
            },
        ]
        msg = 'Player instance mismatch (name, competition)'
        self.assertListEqual(sorted(received,
                                    key=lambda x: x.get('name')),
                             expected,
                             msg)

    def test_get_players_multiple(self):
        """Players lookup: multiple.
        """
        # Given a player name
        name = ['Eboni Amos', 'Zoe Allen']

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = json.dumps(reporter.get_players(name))
        received = json_loads_byteified(received)

        # then I should get the player profile
        with open(os.path.join(self.__results_dir,
                               'players_multiple_names.json')) as _fh:
            expected = json_loads_byteified(_fh.read().strip())
        msg = 'Players lookup (multiple name query) mismatch'
        self.assertListEqual(sorted(received,
                                    key=operator.itemgetter(b'name',
                                                            b'section')),
                             expected,
                             msg)

    def test_get_teams(self):
        """Get unique list of sorted teams.
        """
        # When I scan for a unique list of teams
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_teams()

        # then I should get a list of ordered teams
        expected = u'Watsonia'
        msg = 'Team scan error'
        self.assertEqual(received[54], expected, msg)

    def test_get_teams_girls_12(self):
        """Get unique list of sorted teams: girls section 12.
        """
        # Given a "girls" competition type
        competition_type = 'girls'

        # and a "section" number 12
        section = 12

        # when I scan for a unique list of teams
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {
            'competition_type': competition_type,
            'section': section
        }
        received = reporter.get_teams(**kwargs)

        # then I should get a list of ordered teams
        expected = [
            'Bundoora',
            'Eaglemont',
            'Mill Park',
            'Rosanna',
            'SJCTC',
            'St Marys',
            'Watsonia',
            'Yallambie'
        ]
        msg = 'Team scan error: girls section 12'
        self.assertListEqual(received, expected, msg)

    def test_get_sections_girls(self):
        """Get unique list of sorted sections: girls.
        """
        # Given a "girls" competition type
        competition_type = 'girls'

        # when I scan for a unique list of teams
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {'competition_type': competition_type}
        received = reporter.get_sections(**kwargs)

        # then I should get a list of ordered teams
        expected = list(range(1, 15))
        msg = 'Section scan error: girls'
        self.assertListEqual(received, expected, msg)

    def test_get_sections_boys(self):
        """Get unique list of sorted sections: boys.
        """
        # Given a "boys" competition type
        competition_type = 'boys'

        # when I scan for a unique list of teams
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {'competition_type': competition_type}
        received = reporter.get_sections(**kwargs)

        # then I should get a list of ordered teams
        expected = list(range(1, 27))
        msg = 'Section scan error: boys'
        self.assertListEqual(received, expected, msg)

    def test_get_sections_default(self):
        """Get unique list of sorted sections: default.
        """
        # Given a default competition type
        competition_type = None

        # when I scan for a unique list of teams
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {'competition_type': competition_type}
        received = reporter.get_sections(**kwargs)

        # then I should get a list of ordered teams
        expected = list(range(1, 27))
        msg = 'Section scan error: default'
        self.assertListEqual(received, expected, msg)

    def test_player_cache_match_all_players(self):
        """Player cache: all players.
        """
        # Given the complete player dataset
        names = None

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = len(reporter.get_players(names))

        # then I should get the player profile
        expected = 7882
        msg = 'Player instance (all players) incorrect count'
        self.assertEqual(received, expected, msg)

    def test_last_fixture_played_grand_final(self):
        """Get the last fixtures associated with a player: grand final.
        """
        # Given a player's game aggregate
        reporter = trols_stats.interface.Reporter(db=self._model)
        token = ('Isabella Markovski~Watsonia Blue~'
                 '14~girls~nejta_saturday_am_autumn_2015')
        game_aggregates = reporter.get_player_fixtures(token)
        print([x() for x in game_aggregates])

        # when I search for the player's last fixture
        last_fixture = reporter.last_fixture_played(game_aggregates)
        received = json.dumps([x() for x in last_fixture])
        received = json_loads_byteified(received)

        # then I should receive a list of fixtures that player was part of
        with open(os.path.join(self.__results_dir,
                               'ise_last_game_aggregates.json')) as _fh:
            expected = json_loads_byteified(_fh.read().strip())
        msg = 'Last fixture (Grand Final) error'
        self.assertEqual(received, expected, msg)

    def test_last_fixture_played_semi_final(self):
        """Get the last fixtures associated with a player: semi final.
        """
        # Given a player's game aggregate
        reporter = trols_stats.interface.Reporter(db=self._model)
        token = ('Zara Simiele~Bundoora~14~girls~'
                 'nejta_saturday_am_autumn_2015')
        game_aggregates = reporter.get_player_fixtures(token)

        # when I search for the player's last fixture
        last_fixture = reporter.last_fixture_played(game_aggregates)

        # then I should receive a list of fixtures
        received = json.dumps([x() for x in last_fixture],
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        with open(os.path.join(self.__results_dir,
                               'zara_last_game_aggregates.json')) as _fh:
            expected = _fh.read().strip()
        msg = 'Last fixture (Semi Final) error'
        self.assertEqual(received, expected, msg)

    def test_get_player_singles_games_no_games_played(self):
        """Get all singles games associated with a player: none played.
        """
        # Given a player name
        player = 'Isabella Markovski'

        # when I search for all of the player's singles games
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_player_singles(player)

        # then I should receive a list of singles games that player was
        # part of
        msg = 'Singles games list (none played) should be empty'
        self.assertListEqual(received, [], msg)

    def test_get_player_doubles_games_all_games_doubles(self):
        """Get all doubles games associated with a player: all doubles.
        """
        # Given a player name
        player = ('Isabella Markovski~Watsonia Blue~14~girls~'
                  'nejta_saturday_am_autumn_2015')

        # when I search for all of the player's doubles games
        reporter = trols_stats.interface.Reporter(db=self._model)
        doubles_games = reporter.get_player_doubles(player)

        # then I should receive a list of doubles games that player was
        # part of
        received = [x() for x in doubles_games][1]
        expected = {
            'fixture': {
                'away_team': 'Watsonia Blue',
                'competition': 'nejta_saturday_am_autumn_2015',
                'competition_type': 'girls',
                'date': '31 Jan 15',
                'home_team': 'St Marys',
                'match_round': 1,
                'section': 14,
                'uid': None
            },
            'opposition': [
                {
                    'name': 'Lauren Amsing',
                    'team': 'St Marys',
                    'uid': None
                },
                {
                    'name': 'Lucinda Ford',
                    'team': 'St Marys',
                    'uid': None
                }
            ],
            'player': {
                'name': 'Isabella Markovski',
                'team': 'Watsonia Blue',
                'uid': None
            },
            'score_against': 6,
            'score_for': 0,
            'team_mate': {
                'name': 'Lily Matt',
                'team': 'Watsonia Blue',
                'uid': None
            },
            'uid': None
        }
        msg = 'Player doubles games (all doubles played) error'
        self.assertDictEqual(received, expected, msg)

    def test_get_player_singles_games_played(self):
        """Get all singles games associated with a player.
        """
        # Given a player name
        player = ('Kristen Fisher~Eltham~1~girls~'
                  'nejta_saturday_am_autumn_2015')

        # when I search for all of the player's singles games
        reporter = trols_stats.interface.Reporter(db=self._model)
        singles_games = reporter.get_player_singles(player)

        # then I should receive a list of singles games that player was
        # part of
        received = json.dumps([x() for x in singles_games])
        received = json_loads_byteified(received)
        with open(os.path.join(self.__results_dir,
                               'kristen_singles_aggregates.json')) as _fh:
            expected = json_loads_byteified(_fh.read().strip())
        msg = 'Singles games list error'
        self.assertEqual(received, expected, msg)

    def test_get_player_doubles_games_played(self):
        """Get all doubles games associated with a player.
        """
        # Given a player name
        player = ('Kristen Fisher~Eltham~1~girls~'
                  'nejta_saturday_am_autumn_2015')

        # when I search for all of the player's doubles games
        reporter = trols_stats.interface.Reporter(db=self._model)
        doubles_games = reporter.get_player_doubles(player)

        # then I should receive a list of doubles games that player was
        # part of
        received = [x() for x in doubles_games]
        msg = 'Doubles trols_stats.model.aggregate.Game count error'
        self.assertEqual(len(received), 8, msg)

        # and and item from the data structure should match
        expected = {
            'opposition': [
                {
                    'name': 'Indiana Pisasale',
                    'uid': None,
                    'team': 'Norris Bank'
                },
                {
                    'name': 'Sasha Pecanic',
                    'uid': None,
                    'team': 'Norris Bank'
                }
            ],
            'uid': None,
            'team_mate': {
                'name': 'Paris Batchelor',
                'uid': None,
                'team': 'Eltham'
            },
            'score_for': 6,
            'player': {
                'name': 'Kristen Fisher',
                'uid': None,
                'team': 'Eltham'
            },
            'fixture': {
                'away_team': 'Eltham',
                'home_team': 'Norris Bank',
                'uid': None,
                'competition_type': 'girls',
                'match_round': 4,
                'section': 1,
                'date': '21 Feb 15',
                'competition': 'nejta_saturday_am_autumn_2015'
            },
            'score_against': 0
        }
        msg = 'Doubles games list error (1st item)'
        self.assertEqual(received[1], expected, msg)

    def test_get_player_stats(self):
        """Get all game stats associated with a player: doubles.
        """
        # Given a player token
        player = ['Kristen Fisher~Eltham~1~girls~'
                  'nejta_saturday_am_autumn_2015']

        # when I calculate the player stats
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_player_stats(player)

        # then I should get a stats structure
        expected = {
            'Kristen Fisher~Eltham~1~girls~'
            'nejta_saturday_am_autumn_2015': {
                'comp': 'nejta_saturday_am_autumn_2015',
                'comp_string': 'NEJTA Saturday AM Autumn 2015',
                'comp_type': 'girls',
                'doubles': {
                    'games_lost': 1,
                    'games_played': 8,
                    'games_won': 7,
                    'percentage': 229.99999999999997,
                    'score_against': 20,
                    'score_for':46
                },
                'name': 'Kristen Fisher',
                'section': '1',
                'singles': {
                    'games_lost': 0,
                    'games_played': 4,
                    'games_won': 4,
                    'percentage': 342.85714285714283,
                    'score_against': 7,
                    'score_for': 24
                },
                'team': 'Eltham',
                'token': 'Kristen Fisher~Eltham~1~girls~'
                         'nejta_saturday_am_autumn_2015',
            }
        }
        msg = 'Player games stats error: doubles'
        self.assertDictEqual(received, expected, msg)

    def test_get_player_stats_with_last_fixture(self):
        """Get all game stats associated with a player: doubles.
        """
        # Given a player token
        player = ['Kristen Fisher~Eltham~1~girls~'
                  'nejta_saturday_am_autumn_2015']

        # when I calculate the player stats
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_player_stats(player, last_fixture=True)

        # then I should get a stats structure
        with open(os.path.join(self.__results_dir,
                               'kristen_stats_with_last_fixture.json')) as _fh:
            expected = json.loads(_fh.read().strip())
        msg = 'Player stats with last fixture'
        self.assertDictEqual(received, expected, msg)

    def test_get_player_stats_with_last_doubles_fixture(self):
        """Get game stats associated with a player: doubles last fixture.
        """
        # Given a player token
        player = ['Kristen Fisher~Eltham~1~girls~'
                  'nejta_saturday_am_autumn_2015']

        # when I calculate the player stats
        reporter = trols_stats.interface.Reporter(db=self._model)
        result = reporter.get_player_stats(player,
                                           last_fixture=True,
                                           event='doubles')

        # then I should get a stats structure with a subset "last_fixture"
        # filename = 'kristen_stats_with_last_doubles_fixture.json'
        # with open(os.path.join(self.__results_dir, filename)) as _fh:
        #     expected = json.loads(_fh.read().strip())
        received = result.get(player[0]).get('last_fixture')
        expected = [
            {
                'fixture': {
                    'away_team': 'Eltham',
                    'competition': 'nejta_saturday_am_autumn_2015',
                    'competition_type': 'girls',
                    'date': '16 May 15',
                    'home_team': 'St Lukes Blue',
                    'match_round': 12,
                    'section': 1,
                    'uid': None
                },
                'opposition': [
                    {
                        'name': 'Natalia Poposka',
                        'team': 'St Lukes Blue',
                        'uid': None
                    },
                    {
                        'name': 'Jamie Lyons',
                        'team': 'St Lukes Blue',
                        'uid': None,
                    }
                ],
                'player': {
                    'name': 'Kristen Fisher',
                    'team': 'Eltham',
                    'uid': None
                },
                'score_against': 2,
                'score_for': 6,
                'team_mate': {
                    'name': 'Julia Cinel',
                    'team': 'Eltham',
                    'uid': None
                },
                'uid': None
            },
            {
                'fixture': {
                    'away_team': 'Eltham',
                    'competition': 'nejta_saturday_am_autumn_2015',
                    'competition_type': 'girls',
                    'date': '16 May 15',
                    'home_team': 'St Lukes Blue',
                    'match_round': 12,
                    'section': 1,
                    'uid': None
                },
                'opposition': [
                    {
                        'name': 'Jamie Lyons',
                        'team': 'St Lukes Blue',
                        'uid': None
                    },
                    {
                        'name': 'Evie Loughnan',
                        'team': 'St Lukes Blue',
                        'uid': None
                    }
                ],
                'player': {
                    'name': 'Kristen Fisher',
                    'team': 'Eltham',
                    'uid': None
                },
                'score_against': 3,
                'score_for': 6,
                'team_mate': {
                    'name': 'Paris Batchelor',
                    'team': 'Eltham',
                    'uid': None
                },
                'uid': None
            }
        ]
        msg = 'Player stats with last fixture'
        self.assertListEqual(received, expected, msg)

    def test_get_player_stats_with_last_singles_fixture(self):
        """Get game stats associated with a player: singles last fixture.
        """
        # Given a player token
        player = ['Kristen Fisher~Eltham~1~girls~'
                  'nejta_saturday_am_autumn_2015']

        # when I calculate the player stats
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_player_stats(player,
                                             last_fixture=True,
                                             event='singles')

        # then I should get a stats structure
        filename = 'kristen_stats_with_last_singles_fixture.json'
        with open(os.path.join(self.__results_dir, filename)) as _fh:
            expected = json.loads(_fh.read())
        msg = 'Player stats with last fixture'
        self.assertDictEqual(received, expected, msg)

    def test_sort_stats_girls_singles_score_for(self):
        """Get sorted stats: girls singles score for.
        """
        # Given the players NEJTA Autumn 2015
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {
            'competition': 'nejta_saturday_am_autumn_2015',
            'competition_type': 'girls'
        }
        players = reporter.get_players(**kwargs)
        player_tokens = [x.get('token') for x in players]
        statistics = reporter.get_player_stats(player_tokens)

        # when I filter on the players game score for
        key = 'score_for'

        # limited to 3 players
        limit = 3

        # when I generate the player stats
        received = reporter.sort_stats(statistics,
                                       event='singles',
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Whitney Guan~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Whitney Guan',
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Whitney Guan~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 7,
                        'games_played': 30,
                        'games_won': 23,
                        'percentage': 190.47619047619045,
                        'score_against': 84,
                        'score_for': 160
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 15,
                        'games_won': 15,
                        'percentage': 428.57142857142856,
                        'score_against': 21,
                        'score_for': 90
                    }
                }
            ),
            (
                'Rachelle Papantuono~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Rachelle Papantuono',
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Rachelle Papantuono~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 30,
                        'games_won': 27,
                        'percentage': 211.24999999999997,
                        'score_against': 80,
                        'score_for': 169
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 15,
                        'games_won': 14,
                        'percentage': 366.66666666666663,
                        'score_against': 24,
                        'score_for': 88
                    }
                }
            ),
            (
                'Maeve Suter~Montmorency~5~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Maeve Suter',
                    'team': 'Montmorency',
                    'section': '5',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Maeve Suter~Montmorency~5~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 28,
                        'games_won': 25,
                        'percentage': 195.06172839506172,
                        'score_against': 81,
                        'score_for': 158
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'percentage': 237.14285714285714,
                        'score_against': 35,
                        'score_for': 83
                    }
                }
            )
        ]
        msg = 'Player games stats (score_for, sorted, singles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_singles_girls_score_for(self):
        """Get sorted stats: singles girls score for.
        """
        # Given the statistics for all girl players
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {
            'competition': 'nejta_saturday_am_autumn_2015',
            'competition_type': 'girls',
        }
        players = reporter.get_players(**kwargs)
        player_tokens = [x.get('token') for x in players]
        statistics = reporter.get_player_stats(player_tokens)

        # when I filter on the players game score for
        key = 'score_for'

        # limited to 5 players
        limit = 3

        # when I generate the player stats
        received = reporter.sort_stats(statistics,
                                       event='singles',
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Whitney Guan~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Whitney Guan',
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token':
                        'Whitney Guan~Clifton~3~girls~'
                        'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 7,
                        'games_played': 30,
                        'games_won': 23,
                        'percentage': 190.47619047619045,
                        'score_against': 84,
                        'score_for': 160
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 15,
                        'games_won': 15,
                        'percentage': 428.57142857142856,
                        'score_against': 21,
                        'score_for': 90
                    }
                }
            ),
            (
                'Rachelle Papantuono~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Rachelle Papantuono',
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token':
                        'Rachelle Papantuono~Clifton~3~girls~'
                        'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 30,
                        'games_won': 27,
                        'percentage': 211.24999999999997,
                        'score_against': 80,
                        'score_for': 169
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 15,
                        'games_won': 14,
                        'percentage': 366.66666666666663,
                        'score_against': 24,
                        'score_for': 88
                    }
                }
            ),
            (
                'Maeve Suter~Montmorency~5~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'comp_type': 'girls',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 28,
                        'games_won': 25,
                        'percentage': 195.06172839506172,
                        'score_against': 81,
                        'score_for': 158
                    },
                    'name': 'Maeve Suter',
                    'section': '5',
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'percentage': 237.14285714285714,
                        'score_against': 35,
                        'score_for': 83
                    },
                    'team': 'Montmorency',
                    'token':
                        'Maeve Suter~Montmorency~5~girls~'
                        'nejta_saturday_am_autumn_2015'
                }
            )
        ]
        msg = 'Player games stats (score_for, sorted, singles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_singles_girls_14_percentage(self):
        """Get sorted stats: singles girls score for.
        """
        # Given the statistics for all players
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {
            'competition': 'nejta_saturday_am_autumn_2015',
            'competition_type': 'girls',
            'section': 14
        }
        players = reporter.get_players(**kwargs)
        player_tokens = [x.get('token') for x in players]
        statistics = reporter.get_player_stats(player_tokens)

        # when I filter on the players game score for
        key = 'percentage'

        # limited to 5 players
        limit = 5

        # when I generate the player stats
        received = reporter.sort_stats(statistics,
                                       event='doubles',
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Lucinda Ford~St Marys~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Lucinda Ford',
                    'team': 'St Marys',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Lucinda Ford~St Marys~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 20,
                        'games_won': 17,
                        'percentage': 181.66666666666666,
                        'score_against': 60,
                        'score_for': 109
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            ),
            (
                'Emma German~Barry Road~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Emma German',
                    'team': 'Barry Road',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Emma German~Barry Road~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 5,
                        'games_played': 20,
                        'games_won': 15,
                        'percentage': 169.84126984126985,
                        'score_against': 63,
                        'score_for': 107
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            ),
            (
                'Ambra Selih~Barry Road~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Ambra Selih',
                    'team': 'Barry Road',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Ambra Selih~Barry Road~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 2,
                        'games_played': 4,
                        'games_won': 2,
                        'percentage': 161.53846153846155,
                        'score_against': 13,
                        'score_for': 21
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            ),
            (
                'Alicia Lazarovski~Bundoora~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Alicia Lazarovski',
                    'team': 'Bundoora',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Alicia Lazarovski~Bundoora~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 18,
                        'games_won': 15,
                        'percentage': 159.01639344262296,
                        'score_against': 61,
                        'score_for': 97
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            ),
            (
                'Mia Bovalino~St Marys~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Mia Bovalino',
                    'team': 'St Marys',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Mia Bovalino~St Marys~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 4,
                        'games_played': 20,
                        'games_won': 16,
                        'percentage': 157.35294117647058,
                        'score_against': 68,
                        'score_for': 107
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            )
        ]
        msg = 'Player games stats (percentage girls/section/doubles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_singles_percentage(self):
        """Get sorted stats: singles percentage.
        """
        # Given the statistics for all players
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {
            'competition': 'nejta_saturday_am_autumn_2015',
        }
        players = reporter.get_players(**kwargs)
        player_tokens = [x.get('token') for x in players]
        statistics = reporter.get_player_stats(player_tokens)

        # when I filter on the players game score for
        key = 'percentage'

        # limited to 5 players
        limit = 5

        # when I generate the player stats
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.sort_stats(statistics,
                                       event='singles',
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Abbey Goeldner~Bundoora~6~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Abbey Goeldner',
                    'team': 'Bundoora',
                    'section': '6',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Abbey Goeldner~Bundoora~6~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 1,
                        'games_played': 7,
                        'games_won': 6,
                        'percentage': 223.52941176470588,
                        'score_against': 17,
                        'score_for': 38
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 4,
                        'games_won': 3,
                        'percentage': 2000.0,
                        'score_against': 1,
                        'score_for': 20
                    }
                }
            ),
            (
                'Marcus Newnham~Eaglemont~16~boys~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Marcus Newnham',
                    'team': 'Eaglemont',
                    'section': '16',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Marcus Newnham~Eaglemont~16~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 1,
                        'games_played': 16,
                        'games_won': 15,
                        'percentage': 287.8787878787879,
                        'score_against': 33,
                        'score_for': 95
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 8,
                        'games_won': 8,
                        'percentage': 960.0,
                        'score_against': 5,
                        'score_for': 48
                    }
                }
            ),
            (
                'Keane Chu~Mill Park~14~boys~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Keane Chu',
                    'team': 'Mill Park',
                    'section': '14',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Keane Chu~Mill Park~14~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 2,
                        'games_played': 22,
                        'games_won': 20,
                        'percentage': 293.0232558139535,
                        'score_against': 43,
                        'score_for': 126
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 11,
                        'games_won': 11,
                        'percentage': 733.3333333333333,
                        'score_against': 9,
                        'score_for': 66
                    }
                }
            ),
            (
                'Brynn Goddard~Eltham~10~boys~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Brynn Goddard',
                    'team': 'Eltham',
                    'section': '10',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Brynn Goddard~Eltham~10~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 6,
                        'games_played': 24,
                        'games_won': 18,
                        'percentage': 178.08219178082192,
                        'score_against': 73,
                        'score_for': 130
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 12,
                        'games_won': 12,
                        'percentage': 553.8461538461538,
                        'score_against': 13,
                        'score_for': 72
                    }
                }
            ),
            (
                'Jeevan Dhaliwal~Eaglemont~16~boys~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Jeevan Dhaliwal',
                    'team': 'Eaglemont',
                    'section': '16',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Jeevan Dhaliwal~Eaglemont~16~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 22,
                        'games_won': 19,
                        'percentage': 250.0,
                        'score_against': 50,
                        'score_for': 125
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 11,
                        'games_won': 11,
                        'percentage': 550.0,
                        'score_against': 12,
                        'score_for': 66
                    }
                }
            )
        ]
        msg = 'Player games stats (score_for, sorted, singles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_doubles_percentage(self):
        """Get sorted stats: doubles percentage.
        """
        # Given the players NEJTA Autumn 2015
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {
            'competition': 'nejta_saturday_am_autumn_2015'
        }
        players = reporter.get_players(**kwargs)
        player_tokens = [x.get('token') for x in players]
        statistics = reporter.get_player_stats(player_tokens)

        # when I filter on the players game percentage
        key = 'percentage'

        # limited to 5 players
        limit = 5

        # when I generate the player stats
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.sort_stats(statistics,
                                       event='doubles',
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Harrison Ponton~Mill Park~14~boys~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Harrison Ponton',
                    'team': 'Mill Park',
                    'section': '14',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Harrison Ponton~Mill Park~14~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 1,
                        'games_played': 22,
                        'games_won': 21,
                        'percentage': 485.1851851851852,
                        'score_against': 27,
                        'score_for': 131
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 11,
                        'games_won': 10,
                        'percentage': 484.6153846153846,
                        'score_against': 13,
                        'score_for': 63
                    }
                }
            ),
            (
                'Aaron Mathews~Mill Park~14~boys~nejta_saturday_am_autumn_2015',
                {
                    'name': 'Aaron Mathews',
                    'team': 'Mill Park',
                    'section': '14',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Aaron Mathews~Mill Park~14~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 1,
                        'games_played': 22,
                        'games_won': 21,
                        'percentage': 433.3333333333333,
                        'score_against': 30,
                        'score_for': 130
                    },
                    'singles': {
                        'games_lost': 2,
                        'games_played': 11,
                        'games_won': 9,
                        'percentage': 246.15384615384616,
                        'score_against': 26,
                        'score_for': 64
                    }
                }
            ),
            (
                'Max Scuderi~Lalor~23~boys~nejta_saturday_am_autumn_2015',
                {
                    'name': 'Max Scuderi',
                    'team': 'Lalor',
                    'section': '23',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Max Scuderi~Lalor~23~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 1,
                        'games_played': 22,
                        'games_won': 21,
                        'percentage': 371.42857142857144,
                        'score_against': 35,
                        'score_for': 130
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    }
                }
            ),
            (
                'Joel Cutajar~Regent~24~boys~nejta_saturday_am_autumn_2015',
                {
                    'name': 'Joel Cutajar',
                    'team': 'Regent',
                    'section': '24',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Joel Cutajar~Regent~24~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 0,
                        'games_played': 12,
                        'games_won': 12,
                        'percentage': 342.85714285714283,
                        'score_against': 21,
                        'score_for': 72
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    }
                }
            ),
            (
                'Matthew Kinglsey~Barry Road~25~boys~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Matthew Kinglsey',
                    'team': 'Barry Road',
                    'section': '25',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Matthew Kinglsey~Barry Road~25~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 1,
                        'games_played': 12,
                        'games_won': 11,
                        'percentage': 304.34782608695656,
                        'score_against': 23,
                        'score_for': 70
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    }
                }
            )
        ]
        msg = 'Player games stats (score_for, sorted, doubles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_singles_score_against(self):
        """Get sorted stats: singles score against.
        """
        # Given the statistics for all players
        reporter = trols_stats.interface.Reporter(db=self._model)
        kwargs = {
            'competition': 'nejta_saturday_am_autumn_2015'
        }
        players = reporter.get_players(**kwargs)
        player_tokens = [x.get('token') for x in players]
        statistics = reporter.get_player_stats(player_tokens)

        # when I filter on the player's game score against
        key = 'score_against'

        # limited to 5 players
        limit = 2

        # when I generate the player stats
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.sort_stats(statistics,
                                       event='singles',
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Callum Northover~ECCA~5~boys~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Callum Northover',
                    'team': 'ECCA',
                    'section': '5',
                    'comp_type': 'boys',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Callum Northover~ECCA~5~boys~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 17,
                        'games_played': 27,
                        'games_won': 10,
                        'percentage': 93.84615384615384,
                        'score_against': 130,
                        'score_for': 122
                    },
                    'singles': {
                        'games_lost': 11,
                        'games_played': 14,
                        'games_won': 3,
                        'percentage': 61.53846153846154,
                        'score_against': 78,
                        'score_for': 48
                    }
                }
            ),
            (
                'Aleesia Sotiropoulos~View Bank~5~'
                'girls~nejta_saturday_am_autumn_2015',
                {
                    'name': 'Aleesia Sotiropoulos',
                    'team': 'View Bank',
                    'section': '5',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Aleesia Sotiropoulos~View Bank~5~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 22,
                        'games_played': 26,
                        'games_won': 4,
                        'percentage': 54.729729729729726,
                        'score_against': 148,
                        'score_for': 81
                    },
                    'singles': {
                        'games_lost': 11,
                        'games_played': 13,
                        'games_won': 2,
                        'percentage': 58.666666666666664,
                        'score_against': 75,
                        'score_for': 44
                    }
                }
            ),
        ]
        msg = 'Player games stats (score_for, sorted, singles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_doubles_team_and_section(self):
        """Get sorted stats: doubles team and section.
        """
        # Given the players for a section based team
        reporter = trols_stats.interface.Reporter(db=self._model)
        players = reporter.get_players(team='Watsonia Blue',
                                       section=14)
        player_tokens = [x.get('token') for x in players]

        # and their match statistics
        statistics = reporter.get_player_stats(player_tokens)

        # and I filter on the players game win/loss percentages
        key = 'percentage'

        # when I generate the player doubles stats
        received = reporter.sort_stats(statistics,
                                       event='doubles',
                                       key=key, reverse=True)

        # then I should get a list of ordered stats
        expected = [
            (
                'Isabella Markovski~Watsonia Blue~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Isabella Markovski',
                    'team': 'Watsonia Blue',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Isabella Markovski~Watsonia Blue~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 8,
                        'games_played': 22,
                        'games_won': 14,
                        'percentage': 152.7027027027027,
                        'score_against': 74,
                        'score_for': 113
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            ),
            (
                'Stephanie Lia~Watsonia Blue~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Stephanie Lia',
                    'team': 'Watsonia Blue',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Stephanie Lia~Watsonia Blue~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 10,
                        'games_played': 22,
                        'games_won': 12,
                        'percentage': 122.98850574712642,
                        'score_against': 87,
                        'score_for': 107
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            ),
            (
                'Eboni Amos~Watsonia Blue~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Eboni Amos',
                    'team': 'Watsonia Blue',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Eboni Amos~Watsonia Blue~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 11,
                        'games_played': 20,
                        'games_won': 9,
                        'percentage': 104.59770114942528,
                        'score_against': 87,
                        'score_for': 91
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            ),
            (
                'Lily Matt~Watsonia Blue~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Lily Matt',
                    'team': 'Watsonia Blue',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Lily Matt~Watsonia Blue~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 8,
                        'games_played': 16,
                        'games_won': 8,
                        'percentage': 101.5625,
                        'score_against': 64,
                        'score_for': 65
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            ),
            (
                'Maddison Hollyoak~Watsonia Blue~14~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Maddison Hollyoak',
                    'team': 'Watsonia Blue',
                    'section': '14',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Maddison Hollyoak~Watsonia Blue~14~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 13,
                        'games_played': 16,
                        'games_won': 3,
                        'percentage': 59.09090909090909,
                        'score_against': 88,
                        'score_for': 52
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 0,
                        'games_won': 0,
                        'percentage': 0.0,
                        'score_against': 0,
                        'score_for': 0
                    },
                }
            )
        ]
        msg = 'Player games stats (team/section/doubles percentage) error'
        self.assertListEqual(received, expected, msg)

    def test_get_player_results_compact(self):
        """Get all match results associated with a player.
        """
        # Given a player name
        player = ['Isabella Markovski~Watsonia Blue~14~girls~'
                  'nejta_saturday_am_autumn_2015']

        # when I search for all of the player's results
        reporter = trols_stats.interface.Reporter(db=self._model)
        results = reporter.get_player_results_compact(player)

        # then I should receive a dict of results that player was
        # part of
        received = list(results.get(player[0])['rounds'])
        expected = [
            1, 2, 4, 7, 8, 9, 10, 12, 14, 'Semi Final', 'Grand Final'
        ]
        msg = 'Match results error'
        self.assertListEqual(received, expected, msg)

    def test_get_player_results_compact_no_match(self):
        """Get all match results associated with a player: no match.
        """
        # Given a player name
        player = ['Isabella Markovski~Watsonia~14~girls~'
                  'nejta_saturday_am_autumn_2015']

        # when I search for all of the player's results
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_player_results_compact(player)

        # then I should receive a dict of results that player was
        # part of
        expected = {
            'Isabella Markovski~Watsonia~14~girls~'
            'nejta_saturday_am_autumn_2015': {
                'rounds': {}
            }
        }
        msg = 'Match results error'
        self.assertDictEqual(received, expected, msg)

    def test_get_competition_details(self):
        """Get all match results associated with a player: no match.
        """
        # Given a competiton token
        competition = 'dvta_tuesday_night_spring_2016'

        # when I get the competition details
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_competition_details(competition)

        # then I should receive a matchin dictionary
        expected = {
            'event': ['doubles'],
            'event_type': ['mens'],
        }
        msg = 'Competion details error'
        self.assertDictEqual(received, expected, msg)

    def test_get_competition_details_nejta(self):
        """Get all match results associated with a player: no match.
        """
        # Given a competiton token
        competition = 'nejta_saturday_am_spring_2016'

        # when I get the competition details
        reporter = trols_stats.interface.Reporter(db=self._model)
        received = reporter.get_competition_details(competition)

        # then I should receive a matching dictionary
        expected = {
            'event': ['singles', 'doubles'],
            'event_type': ['girls', 'boys'],
        }
        msg = 'Competion details error'
        self.assertDictEqual(received, expected, msg)

    def test_player_ids_dict(self):
        """Test player_ids_dict.
        """
        # Given a list of player IDs
        players = [
            "John Guanzon~Epping~3~boys~nejta_saturday_am_spring_2015",
            "Whitney Guan~Clifton~2~girls~nejta_saturday_am_spring_2015",
        ]

        # when I convert to a dictionary structure
        received = trols_stats.interface.Reporter.player_ids_dict(players)

        # then I should receive the correct list of dictionaries
        expected = [
            {
                'comp': 'nejta_saturday_am_spring_2015',
                'comp_string': 'NEJTA Saturday AM Spring 2015',
                'comp_type': 'boys',
                'name': 'John Guanzon',
                'section': '3',
                'team': 'Epping',
                'token': 'John Guanzon~Epping~3~boys~'
                         'nejta_saturday_am_spring_2015'
            },
            {
                'comp': 'nejta_saturday_am_spring_2015',
                'comp_string': 'NEJTA Saturday AM Spring 2015',
                'comp_type': 'girls',
                'name': 'Whitney Guan',
                'section': '2',
                'team': 'Clifton',
                'token': 'Whitney Guan~Clifton~2~girls~'
                         'nejta_saturday_am_spring_2015'
            }
        ]
        msg = 'Player IDs to dict conversion error'
        self.assertListEqual(received, expected, msg)

    def test_rank_stats_singles_score_for(self):
        """Rank stats for singles events across the "score_for" key.
        """
        # Given a list of "score_for" ordered singles
        statistics = [
            (
                'Whitney Guan~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Whitney Guan',
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Whitney Guan~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 7,
                        'games_played': 30,
                        'games_won': 23,
                        'percentage': 190.47619047619045,
                        'score_against': 84,
                        'score_for': 160
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 15,
                        'games_won': 15,
                        'percentage': 428.57142857142856,
                        'score_against': 21,
                        'score_for': 90
                    }
                }
            ),
            (
                'Rachelle Papantuono~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Rachelle Papantuono',
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Rachelle Papantuono~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 30,
                        'games_won': 27,
                        'percentage': 211.24999999999997,
                        'score_against': 80,
                        'score_for': 169
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 15,
                        'games_won': 14,
                        'percentage': 366.66666666666663,
                        'score_against': 24,
                        'score_for': 88
                    }
                }
            ),
            (
                'Maeve Suter~Montmorency~5~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Maeve Suter',
                    'team': 'Montmorency',
                    'section': '5',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Maeve Suter~Montmorency~5~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 28,
                        'games_won': 25,
                        'percentage': 195.06172839506172,
                        'score_against': 81,
                        'score_for': 158
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'percentage': 237.14285714285714,
                        'score_against': 35,
                        'score_for': 83
                    }
                }
            )
        ]

        # when I rank on the players game score for
        kwargs = {
            'event': 'singles',
            'key': 'score_for'
        }
        received = trols_stats.interface.Reporter.rank_stats(statistics,
                                                             **kwargs)

        # then I should get a list of ranked stats
        expected = [
            (
                'Whitney Guan~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Whitney Guan',
                    'rank': 1,
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Whitney Guan~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 7,
                        'games_played': 30,
                        'games_won': 23,
                        'percentage': 190.47619047619045,
                        'score_against': 84,
                        'score_for': 160
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 15,
                        'games_won': 15,
                        'percentage': 428.57142857142856,
                        'score_against': 21,
                        'score_for': 90
                    }
                }
            ),
            (
                'Rachelle Papantuono~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Rachelle Papantuono',
                    'rank': 2,
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Rachelle Papantuono~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 30,
                        'games_won': 27,
                        'percentage': 211.24999999999997,
                        'score_against': 80,
                        'score_for': 169
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 15,
                        'games_won': 14,
                        'percentage': 366.66666666666663,
                        'score_against': 24,
                        'score_for': 88
                    }
                }
            ),
            (
                'Maeve Suter~Montmorency~5~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Maeve Suter',
                    'rank': 3,
                    'team': 'Montmorency',
                    'section': '5',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Maeve Suter~Montmorency~5~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 28,
                        'games_won': 25,
                        'percentage': 195.06172839506172,
                        'score_against': 81,
                        'score_for': 158
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'percentage': 237.14285714285714,
                        'score_against': 35,
                        'score_for': 83
                    }
                }
            )
        ]
        msg = 'Player ranked stats (score_for, sorted, singles) error'
        self.assertListEqual(received, expected, msg)

    def test_rank_stats_singles_percentage_grouped_ranking(self):
        """Group rank stats for singles events across the "percentage" key.
        """
        # Given a list of "percentage" ordered singles
        statistics = [
            (
                'Whitney Guan~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Whitney Guan',
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Whitney Guan~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 7,
                        'games_played': 30,
                        'games_won': 23,
                        'percentage': 190.47619047619045,
                        'score_against': 84,
                        'score_for': 160
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 15,
                        'games_won': 15,
                        'percentage': 450,
                        'score_against': 20,
                        'score_for': 90
                    }
                }
            ),
            (
                'Rachelle Papantuono~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Rachelle Papantuono',
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Rachelle Papantuono~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 30,
                        'games_won': 27,
                        'percentage': 211.24999999999997,
                        'score_against': 80,
                        'score_for': 169
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 15,
                        'games_won': 14,
                        'percentage': 450,
                        'score_against': 20,
                        'score_for': 90 
                    }
                }
            ),
            (
                'Maeve Suter~Montmorency~5~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Maeve Suter',
                    'team': 'Montmorency',
                    'section': '5',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Maeve Suter~Montmorency~5~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 28,
                        'games_won': 25,
                        'percentage': 195.06172839506172,
                        'score_against': 81,
                        'score_for': 158
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'percentage': 237.14285714285714,
                        'score_against': 35,
                        'score_for': 83
                    }
                }
            )
        ]

        # when I rank on the players game score for
        kwargs = {
            'event': 'singles',
            'key': 'percentage'
        }
        received = trols_stats.interface.Reporter.rank_stats(statistics,
                                                             **kwargs)

        # then I should get a list of ranked stats
        expected = [
            (
                'Whitney Guan~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Whitney Guan',
                    'rank': 1,
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Whitney Guan~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 7,
                        'games_played': 30,
                        'games_won': 23,
                        'percentage': 190.47619047619045,
                        'score_against': 84,
                        'score_for': 160
                    },
                    'singles': {
                        'games_lost': 0,
                        'games_played': 15,
                        'games_won': 15,
                        'percentage': 450,
                        'score_against': 20,
                        'score_for': 90
                    }
                }
            ),
            (
                'Rachelle Papantuono~Clifton~3~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Rachelle Papantuono',
                    'rank': 1,
                    'team': 'Clifton',
                    'section': '3',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Rachelle Papantuono~Clifton~3~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 30,
                        'games_won': 27,
                        'percentage': 211.24999999999997,
                        'score_against': 80,
                        'score_for': 169
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 15,
                        'games_won': 14,
                        'percentage': 450,
                        'score_against': 20,
                        'score_for': 90 
                    }
                }
            ),
            (
                'Maeve Suter~Montmorency~5~girls~'
                'nejta_saturday_am_autumn_2015',
                {
                    'name': 'Maeve Suter',
                    'rank': 3,
                    'team': 'Montmorency',
                    'section': '5',
                    'comp_type': 'girls',
                    'comp': 'nejta_saturday_am_autumn_2015',
                    'comp_string': 'NEJTA Saturday AM Autumn 2015',
                    'token': 'Maeve Suter~Montmorency~5~girls~'
                             'nejta_saturday_am_autumn_2015',
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 28,
                        'games_won': 25,
                        'percentage': 195.06172839506172,
                        'score_against': 81,
                        'score_for': 158
                    },
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'percentage': 237.14285714285714,
                        'score_against': 35,
                        'score_for': 83
                    }
                }
            )
        ]
        msg = 'Player ranked stats (score_for, sorted, singles) error'
        self.assertListEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls._model
        del cls.__results_dir
