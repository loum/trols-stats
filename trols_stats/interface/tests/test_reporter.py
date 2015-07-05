import unittest2
import os
import json

import trols_stats.interface as interface


class TestReporter(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
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
                'team': u'Watsonia Blue'
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
        game_aggrepates = self.__reporter.get_player_fixtures(player)

        # then I should receive a list of fixtures that player was part of
        received = json.dumps([x() for x in game_aggrepates],
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        with open(os.path.join(self.__results_dir,
                               'ise_game_aggregates.json')) as _fh:
            expected = _fh.read().strip()
        msg = 'Player combined fixtures output as JSON error'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls.__results_dir
        del cls.__reporter
