import unittest2

import trols_stats


class TestPlayer(unittest2.TestCase):
    def test_init(self):
        """Initialise a trols_stats.Player object.
        """
        player = trols_stats.Player()
        msg = 'Object is not of type trols_stats.Player'
        self.assertIsInstance(player, trols_stats.Player, msg)

    def test_to_json(self):
        """Convert trols_stats.Player() object to JSON.
        """
        player_data = {'player_id': 'xyz',
                       'name': 'Player 1',
                       'team': 'Best team',
                       'competition': 'girls'}
        player = trols_stats.Player(**player_data)

        received = player.to_json()

        expected = '{"team": "Best team", "id": "xyz", "competition": "girls", "name": "Player 1"}'
        msg = 'trols_stats.Player() to JSON error'
        self.assertEqual(received, expected, msg)
