import unittest2
import os
import json

import trols_stats.interface as interface


class TestReporter(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        shelve_dir = os.path.join('trols_stats',
                                  'interface',
                                  'tests',
                                  'files')
        cls.__results_dir = os.path.join('trols_stats',
                                         'interface',
                                         'tests',
                                         'results')

        cls.__reporter = interface.Reporter(shelve=shelve_dir)

    def test_init(self):
        """Initialise an interface.Reporter object
        """
        msg = 'Object is not a interface.Reporter'
        self.assertIsInstance(self.__reporter, interface.Reporter, msg)

    def test_player_cache_player_match(self):
        """Player cache: player match.
        """
        # Given a Games store

        # when I query a player
        received = self.__reporter.get_players('Eboni Amos')

        # then I should get the player profile
        expected = [
            {
                'name': 'Eboni Amos',
                'section': 14,
                'team': u'Watsonia Blue',
                'token': 'Eboni Amos|Watsonia Blue|14'
            },
        ]
        msg = 'Player cache mismatch'
        self.assertListEqual(received, expected, msg)

    def test_player_cache_match_all_players(self):
        """Player cache: all players.
        """
        # Given a Games store

        # when I query a player
        received = len(self.__reporter.get_players())

        # then I should get the player profile
        expected = 1905
        msg = 'Player cache incorrect count'
        self.assertEqual(received, expected, msg)

    def test_get_player_fixtures(self):
        """Get all fixtures associated with a player.
        """
        # Given a player name
        player = 'Isabella Markovski'

        # when I search for all of the player's fixtures
        game_aggregates = self.__reporter.get_player_fixtures(player)

        # then I should receive a list of fixtures that player was part of
        received = json.dumps([x() for x in game_aggregates],
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        with open(os.path.join(self.__results_dir,
                               'ise_game_aggregates.json')) as _fh:
            expected = _fh.read().strip()
        msg = 'Player combined fixtures output as JSON error'
        self.assertEqual(received, expected, msg)

    def test_get_player_singles_games_no_games_played(self):
        """Get all singles games associated with a player: none played.
        """
        # Given a player name
        player = 'Isabella Markovski'

        # when I search for all of the player's singles games
        received = self.__reporter.get_player_singles(player)

        # then I should receive a list of singles games that player was
        # part of
        msg = 'Singles games list (none played) should be empty'
        self.assertListEqual(received, [], msg)

    def test_get_player_doubles_games_all_games_doubles(self):
        """Get all doubles games associated with a player: all doubles.
        """
        # Given a player name
        player = 'Isabella Markovski'

        # when I search for all of the player's doubles games
        doubles_games = self.__reporter.get_player_doubles(player)

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
        self.assertEqual(received, expected, msg)

    def test_get_player_singles_games_played(self):
        """Get all singles games associated with a player.
        """
        # Given a player name
        player = 'Kristen Fisher'

        # when I search for all of the player's singles games
        singles_games = self.__reporter.get_player_singles(player)

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
        self.assertEqual(received, expected, msg)

    def test_get_player_doubles_games_played(self):
        """Get all doubles games associated with a player.
        """
        # Given a player name
        player = 'Kristen Fisher'

        # when I search for all of the player's doubles games
        doubles_games = self.__reporter.get_player_doubles(player)

        # then I should receive a list of singles games that player was
        # part of
        received = json.dumps([x() for x in doubles_games],
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        with open(os.path.join(self.__results_dir,
                               'kristen_doubles_aggregates.json')) as _fh:
            expected = _fh.read().strip()
        msg = 'Doubles games list error'
        self.assertEqual(received, expected, msg)

    def test_get_player_stats(self):
        """Get all game stats associated with a player.
        """
        # Given a player name
        player = 'Kristen Fisher'

        # when I calculate the player stats
        received = self.__reporter.get_player_stats(player)

        # then I should get a stats structure
        expected = {
            'Kristen Fisher|Eltham|1': {
                'doubles': {
                    'games_lost': 1,
                    'games_played': 8,
                    'games_won': 7,
                    'score_against': 20,
                    'score_for': 46},
                'singles': {
                    'games_lost': 0,
                    'games_played': 4,
                    'games_won': 4,
                    'score_against': 7,
                    'score_for': 24
                }
            }
        }
        msg = 'Player games stats error'
        self.assertDictEqual(received, expected, msg)

        received = self.__reporter.get_player_stats(player)

    @classmethod
    def tearDownClass(cls):
        del cls.__results_dir
        del cls.__reporter
