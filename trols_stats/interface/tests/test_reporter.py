import unittest2
import os
import json

import trols_stats
import trols_stats.interface


class TestReporter(unittest2.TestCase):
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
        session = trols_stats.DBSession(shelve=shelve_dir)
        session.connect()
        cls.__db = session.connection['trols']

    def test_init(self):
        """Initialise an trols_stats.interface.Reporter object
        """
        reporter = trols_stats.interface.Reporter(db=self.__db)
        msg = 'Object is not a trols_stats.interface.Reporter'
        self.assertIsInstance(reporter, trols_stats.interface.Reporter, msg)

    def test_get_players(self):
        """Players lookup.
        """
        # Given a player name
        name = ['Eboni Amos']

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.get_players(name)

        # then I should get the player profile
        expected = [
            'Eboni Amos|Watsonia Blue|14|girls|saturday_am_autumn_2015',
            'Eboni Amos|Watsonia|12|girls|saturday_am_spring_2015'
        ]
        msg = 'Player instance mismatch'
        self.assertListEqual(received, expected, msg)

    def test_get_players_lowercase(self):
        """Players lookup: lower case.
        """
        # Given a player name with lower casing
        name = ['eboni amos']

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.get_players(names=name)

        # then I should get the player profile
        expected = [
            'Eboni Amos|Watsonia Blue|14|girls|saturday_am_autumn_2015',
            'Eboni Amos|Watsonia|12|girls|saturday_am_spring_2015'
        ]
        msg = 'Player instance mismatch'
        self.assertListEqual(received, expected, msg)

    def test_get_players_lowercase_multiple_part_names(self):
        """Players lookup: lower case.
        """
        # Given a player part names
        names = ['isabella', 'markovski']

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.get_players(names=names)

        # then I should get the player profile
        expected = [
            'Isabella Chessler|Mill Park|11|girls|saturday_am_spring_2015',
            'Isabella Cotroneo|Keon Park|2|girls|saturday_am_autumn_2015',
            'Isabella Grant|Eaglemont|12|girls|saturday_am_autumn_2015',
            'Isabella Markovski|Watsonia Blue|14|girls|saturday_am_autumn_2015',
            'Isabella Markovski|Watsonia|12|girls|saturday_am_spring_2015',
            'Joel Markovski|Watsonia|20|boys|saturday_am_autumn_2015',
            'Joel Markovski|Watsonia|21|boys|saturday_am_spring_2015',
        ]
        msg = 'Part player name instance mismatch'
        self.assertListEqual(sorted(received), expected, msg)

    def test_get_players_team_and_section(self):
        """Players lookup: team and section.
        """
        # Given a team name
        team = 'Watsonia Blue'

        # and a section
        section = 14

        # when I query the players
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.get_players(team=team, section=section)

        # then I should get the player profile
        expected = [
            'Eboni Amos|Watsonia Blue|14|girls|saturday_am_autumn_2015',
            'Isabella Markovski|Watsonia Blue|14|girls|saturday_am_autumn_2015',
            'Lily Matt|Watsonia Blue|14|girls|saturday_am_autumn_2015',
            'Maddison Hollyoak|Watsonia Blue|14|girls|saturday_am_autumn_2015',
            'Stephanie Lia|Watsonia Blue|14|girls|saturday_am_autumn_2015',
        ]
        msg = 'Player instance mismatch'
        self.assertListEqual(sorted(received), expected, msg)

    def test_get_players_multiple(self):
        """Players lookup: multiple.
        """
        # Given a player name
        name = ['Eboni Amos', 'Zoe Allen']

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.get_players(name)

        # then I should get the player profile
        expected = [
            'Eboni Amos|Watsonia Blue|14|girls|saturday_am_autumn_2015',
            'Eboni Amos|Watsonia|12|girls|saturday_am_spring_2015',
            'Zoe Allen|Eaglemont|10|girls|saturday_am_autumn_2015',
            'Zoe Allen|Eaglemont|7|girls|saturday_am_spring_2015',
            'Zoe Allen|Eaglemont|8|girls|saturday_am_autumn_2015',
        ]
        msg = 'Player instance (multiple) mismatch'
        self.assertListEqual(sorted(received), expected, msg)

    def test_player_cache_match_all_players(self):
        """Player cache: all players.
        """
        # Given the complete player dataset
        names = None

        # when I query a player
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = len(reporter.get_players(names))

        # then I should get the player profile
        expected = 3001
        msg = 'Player instance (all players) incorrect count'
        self.assertEqual(received, expected, msg)

    def test_get_player_fixtures(self):
        """Get all fixtures associated with a player.
        """
        # Given a player name
        player = 'Isabella Markovski|Watsonia Blue|14|girls|saturday_am_autumn_2015'

        # when I search for all of the player's fixtures
        reporter = trols_stats.interface.Reporter(db=self.__db)
        game_aggregates = reporter.get_player_fixtures(player)

        # then I should receive a list of fixtures that player was part of
        received = json.dumps([x() for x in game_aggregates],
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))

        with open(os.path.join(self.__results_dir,
                               'ise_game_aggregates.json')) as _fh:
            expected = _fh.read().strip()
        msg = 'Player combined fixtures output as JSON error'
        self.assertEqual(sorted(received), sorted(expected), msg)

    def test_get_player_singles_games_no_games_played(self):
        """Get all singles games associated with a player: none played.
        """
        # Given a player name
        player = 'Isabella Markovski'

        # when I search for all of the player's singles games
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.get_player_singles(player)

        # then I should receive a list of singles games that player was
        # part of
        msg = 'Singles games list (none played) should be empty'
        self.assertListEqual(received, [], msg)

    def test_get_player_doubles_games_all_games_doubles(self):
        """Get all doubles games associated with a player: all doubles.
        """
        # Given a player name
        player = 'Isabella Markovski|Watsonia Blue|14|girls|saturday_am_autumn_2015'

        # when I search for all of the player's doubles games
        reporter = trols_stats.interface.Reporter(db=self.__db)
        doubles_games = reporter.get_player_doubles(player)

        # then I should receive a list of doubles games that player was
        # part of
        received = json.dumps([x() for x in doubles_games],
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        with open(os.path.join(self.__results_dir,
                               'ise_game_aggregates.json')) as _fh:
            expected = _fh.read().strip()
        msg = 'Player doubles games (all doubles played) error'
        self.assertEqual(sorted(received), sorted(expected), msg)

    def test_get_player_singles_games_played(self):
        """Get all singles games associated with a player.
        """
        # Given a player name
        player = 'Kristen Fisher|Eltham|1|girls|saturday_am_autumn_2015'

        # when I search for all of the player's singles games
        reporter = trols_stats.interface.Reporter(db=self.__db)
        singles_games = reporter.get_player_singles(player)

        # then I should receive a list of singles games that player was
        # part of
        received = json.dumps([x() for x in singles_games],
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        with open(os.path.join(self.__results_dir,
                               'kristen_singles_aggregates.json')) as _fh:
            expected = _fh.read().strip()
        msg = 'Singles games list error'
        self.assertEqual(sorted(received), sorted(expected), msg)

    def test_get_player_doubles_games_played(self):
        """Get all doubles games associated with a player.
        """
        # Given a player name
        player = 'Kristen Fisher|Eltham|1|girls|saturday_am_autumn_2015'

        # when I search for all of the player's doubles games
        reporter = trols_stats.interface.Reporter(db=self.__db)
        doubles_games = reporter.get_player_doubles(player)

        # then I should receive a list of singles games that player was
        # part of
        received = json.dumps([x() for x in doubles_games],
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        with open(os.path.join(self.__results_dir,
                               'kristen_doubles_aggregates.json')) as _fh:
            expected = _fh.read().rstrip()
        msg = 'Doubles games list error'
        self.assertEqual(sorted(received), sorted(expected), msg)

    def test_get_player_stats_singles(self):
        """Get all game stats associated with a player: singles.
        """
        # Given a player name
        player = ['Kristen Fisher|Eltham|1|girls|saturday_am_autumn_2015']

        # when I calculate the player stats
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.get_player_stats(player)

        # then I should get a stats structure
        expected = {
            'Kristen Fisher|Eltham|1|girls|saturday_am_autumn_2015': {
                'singles': {
                    'games_lost': 0,
                    'games_played': 4,
                    'games_won': 4,
                    'score_against': 7,
                    'score_for': 24,
                    'percentage': 342.85714285714283
                }
            }
        }
        msg = 'Player games stats error: singles'
        self.assertDictEqual(received, expected, msg)

    def test_get_player_stats_doubles(self):
        """Get all game stats associated with a player: doubles.
        """
        # Given a player token
        player = ['Kristen Fisher|Eltham|1|girls|saturday_am_autumn_2015']

        # and an "doubles" event specified
        event = 'doubles'

        # when I calculate the player stats
        reporter = trols_stats.interface.Reporter(db=self.__db,
                                                  event=event)
        received = reporter.get_player_stats(player)

        # then I should get a stats structure
        expected = {
            'Kristen Fisher|Eltham|1|girls|saturday_am_autumn_2015': {
                'doubles': {
                    'games_lost': 1,
                    'games_played': 8,
                    'games_won': 7,
                    'percentage': 229.99999999999997,
                    'score_against': 20,
                    'score_for':46
                }
            }
        }
        msg = 'Player games stats error: doubles'
        self.assertDictEqual(received, expected, msg)

    def test_sort_stats_singles_score_for(self):
        """Get sorted stats: singles score for.
        """
        # Given the statistics for all players
        reporter = trols_stats.interface.Reporter(db=self.__db)
        stats = reporter.get_player_stats()

        # when I filter on the players game score for
        key = 'score_for'

        # limited to 5 players
        limit = 5

        # when I generate the player stats
        received = reporter.sort_stats(stats,
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Whitney Guan|Clifton|3|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 0,
                        'games_played': 15,
                        'games_won': 15,
                        'score_against': 21,
                        'score_for': 90,
                        'percentage': 428.57142857142856
                    }
                }
            ),
            (
                'Rachelle Papantuono|Clifton|3|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 1,
                        'games_played': 15,
                        'games_won': 14,
                        'score_against': 24,
                        'score_for': 88,
                        'percentage': 366.66666666666663
                    }
                }
            ),
            (
                'Connor Salas|Rosanna|8|boys|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'score_against': 32,
                        'score_for': 83,
                        'percentage': 259.375
                    }
                }
            ),
            (
                'Maeve Suter|Montmorency|5|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'score_against': 35,
                        'score_for': 83,
                        'percentage': 237.14285714285714
                    }
                }
            ),
            (
                'Ethan Turner|ECCA|5|boys|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'score_against': 30,
                        'score_for': 82,
                        'percentage': 273.3333333333333
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
        reporter = trols_stats.interface.Reporter(db=self.__db)
        girls = reporter.get_players(competition_type='girls')
        statistics = reporter.get_player_stats(girls)

        # when I filter on the players game score for
        key = 'score_for'

        # limited to 5 players
        limit = 5

        # when I generate the player stats
        received = reporter.sort_stats(statistics,
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Whitney Guan|Clifton|3|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 0,
                        'games_played': 15,
                        'games_won': 15,
                        'score_against': 21,
                        'score_for': 90,
                        'percentage': 428.57142857142856
                    }
                }
            ),
            (
                'Rachelle Papantuono|Clifton|3|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 1,
                        'games_played': 15,
                        'games_won': 14,
                        'score_against': 24,
                        'score_for': 88,
                        'percentage': 366.66666666666663
                    }
                }
            ),
            (
                'Maeve Suter|Montmorency|5|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 1,
                        'games_played': 14,
                        'games_won': 13,
                        'score_against': 35,
                        'score_for': 83,
                        'percentage': 237.14285714285714
                    }
                }
            ),
            (
                "Emily O'Connor|Clifton|3|girls|saturday_am_autumn_2015",
                {
                    'singles': {
                        'games_lost': 3,
                        'games_played': 15,
                        'games_won': 12,
                        'percentage': 180.0,
                        'score_against': 45,
                        'score_for': 81
                    }
                }
            ),
            (
                'Lauren Jones|Yallambie|4|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 2,
                        'games_played': 14,
                        'games_won': 12,
                        'percentage': 192.85714285714286,
                        'score_against': 42,
                        'score_for': 81
                    }
                }
            )
        ]
        msg = 'Player games stats (score_for, sorted, singles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_singles_girls_14_percentage(self):
        """Get sorted stats: singles girls score for.
        """
        # Given the statistics for all players
        reporter = trols_stats.interface.Reporter(db=self.__db,
                                                  event='doubles')
        girls = reporter.get_players(competition_type='girls',
                                     section=14)
        statistics = reporter.get_player_stats(girls)

        # when I filter on the players game score for
        key = 'percentage'

        # limited to 5 players
        limit = 5

        # when I generate the player stats
        received = reporter.sort_stats(statistics,
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Lucinda Ford|St Marys|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 20,
                        'games_won': 17,
                        'percentage': 181.66666666666666,
                        'score_against': 60,
                        'score_for': 109
                    }
                }
            ),
            (
                'Emma German|Barry Road|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 5,
                        'games_played': 20,
                        'games_won': 15,
                        'percentage': 169.84126984126985,
                        'score_against': 63,
                        'score_for': 107
                    }
                }
            ),
            (
                'Ambra Selih|Barry Road|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 2,
                        'games_played': 4,
                        'games_won': 2,
                        'percentage': 161.53846153846155,
                        'score_against': 13,
                        'score_for': 21
                    }
                }
            ),
            (
                'Alicia Lazarovski|Bundoora|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 3,
                        'games_played': 18,
                        'games_won': 15,
                        'percentage': 159.01639344262296,
                        'score_against': 61,
                        'score_for': 97
                    }
                }
            ),
            (
                'Mia Bovalino|St Marys|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 4,
                        'games_played': 20,
                        'games_won': 16,
                        'percentage': 157.35294117647058,
                        'score_against': 68,
                        'score_for': 107
                    }
                }
            )
        ]
        msg = 'Player games stats (percentage girls/section/doubles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_singles_percentage(self):
        """Get sorted stats: singles percentage.
        """
        # Given the statistics for all players
        reporter = trols_stats.interface.Reporter(db=self.__db)
        statistics = reporter.get_player_stats()

        # when I filter on the players game score for
        key = 'percentage'

        # limited to 5 players
        limit = 5

        # when I generate the player stats
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.sort_stats(statistics,
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Abbey Goeldner|Bundoora|6|girls|saturday_am_autumn_2015',
                {
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
                'Marcus Newnham|Eaglemont|16|boys|saturday_am_autumn_2015',
                {
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
                'Keane Chu|Mill Park|14|boys|saturday_am_autumn_2015',
                {
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
                'Brynn Goddard|Eltham|10|boys|saturday_am_autumn_2015',
                {
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
                'Jeevan Dhaliwal|Eaglemont|16|boys|saturday_am_autumn_2015',
                {
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
        # Given the statistics for all players
        reporter = trols_stats.interface.Reporter(db=self.__db)
        statistics = reporter.get_player_stats()

        # when I filter on the players game percentage
        key = 'percentage'

        # limited to 5 players
        limit = 5

        # when I generate the player stats
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.sort_stats(statistics,
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Abbey Goeldner|Bundoora|6|girls|saturday_am_autumn_2015',
                {
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
                'Marcus Newnham|Eaglemont|16|boys|saturday_am_autumn_2015',
                {
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
                'Keane Chu|Mill Park|14|boys|saturday_am_autumn_2015',
                {
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
                'Brynn Goddard|Eltham|10|boys|saturday_am_autumn_2015',
                {
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
                'Jeevan Dhaliwal|Eaglemont|16|boys|saturday_am_autumn_2015',
                {
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
        msg = 'Player games stats (score_for, sorted, doubles) error'
        self.assertListEqual(received, expected, msg)

    def test_sort_stats_singles_score_against(self):
        """Get sorted stats: singles score against.
        """
        # Given the statistics for all players
        reporter = trols_stats.interface.Reporter(db=self.__db)
        statistics = reporter.get_player_stats()

        # when I filter on the player's game score against
        key = 'score_against'

        # limited to 5 players
        limit = 4

        # when I generate the player stats
        reporter = trols_stats.interface.Reporter(db=self.__db)
        received = reporter.sort_stats(statistics,
                                       key=key,
                                       reverse=True,
                                       limit=limit)

        # then I should get a list of ordered stats
        expected = [
            (
                'Callum Northover|ECCA|5|boys|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 11,
                        'games_played': 14,
                        'games_won': 3,
                        'score_against': 78,
                        'score_for': 48,
                        'percentage': 61.53846153846154
                    }
                }
            ),
            (
                'Aleesia Sotiropoulos|View Bank|5|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 11,
                        'games_played': 13,
                        'games_won': 2,
                        'score_against': 75,
                        'score_for': 44,
                        'percentage': 58.666666666666664
                    }
                }
            ),
            (
                'Adam Walter|Lalor Blue|2|boys|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 11,
                        'games_played': 14,
                        'games_won': 3,
                        'score_against': 73,
                        'score_for': 49,
                        'percentage': 67.12328767123287
                    }
                }
            ),
            (
                'Celeste Argent|Montmorency|2|girls|saturday_am_autumn_2015',
                {
                    'singles': {
                        'games_lost': 8,
                        'games_played': 15,
                        'games_won': 7,
                        'score_against': 73,
                        'score_for': 60,
                        'percentage': 82.1917808219178
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
        reporter = trols_stats.interface.Reporter(db=self.__db,
                                                  event='doubles')
        players = reporter.get_players(team='Watsonia Blue',
                                       section=14)

        # and their match statistics
        statistics = reporter.get_player_stats(players)

        # and I filter on the players game win/loss percentages
        key = 'percentage'

        # when I generate the player doubles stats
        received = reporter.sort_stats(statistics, key=key, reverse=True)

        # then I should get a list of ordered stats
        expected = [
            (
                'Isabella Markovski|Watsonia Blue|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 8,
                        'games_played': 22,
                        'games_won': 14,
                        'percentage': 152.7027027027027,
                        'score_against': 74,
                        'score_for': 113
                    }
                }
            ),
            (
                'Stephanie Lia|Watsonia Blue|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 10,
                        'games_played': 22,
                        'games_won': 12,
                        'percentage': 122.98850574712642,
                        'score_against': 87,
                        'score_for': 107
                    }
                }
            ),
            (
                'Eboni Amos|Watsonia Blue|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 11,
                        'games_played': 20,
                        'games_won': 9,
                        'percentage': 104.59770114942528,
                        'score_against': 87,
                        'score_for': 91
                    }
                }
            ),
            (
                'Lily Matt|Watsonia Blue|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 8,
                        'games_played': 16,
                        'games_won': 8,
                        'percentage': 101.5625,
                        'score_against': 64,
                        'score_for': 65
                    }
                }
            ),
            (
                'Maddison Hollyoak|Watsonia Blue|14|girls|saturday_am_autumn_2015',
                {
                    'doubles': {
                        'games_lost': 13,
                        'games_played': 16,
                        'games_won': 3,
                        'percentage': 59.09090909090909,
                        'score_against': 88,
                        'score_for': 52
                    }
                }
            )
        ]
        msg = 'Player games stats (team/section/doubles percentage) error'
        self.assertListEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls.__db
        del cls.__results_dir
