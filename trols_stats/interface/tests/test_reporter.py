import unittest2
import os

import trols_stats.interface as interface


class TestReporter(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        shelve_dir = os.path.join('trols_stats',
                                  'interface',
                                  'tests',
                                  'files')

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
        received = self.__reporter.get_players('Isabella Markovski')

        # then I should get the player profile
        expected = [
            {
                'name': 'Isabella Markovski',
                'section': 14,
                'team': u'Watsonia Red'
            },
            {
                'name': 'Isabella Markovski',
                'section': 14,
                'team': u'Watsonia Blue'
            }
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
        expected = 3729
        msg = 'Player cache incorrect count'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls.__reporter
