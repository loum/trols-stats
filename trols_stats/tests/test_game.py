import unittest2

import trols_stats


class TestGame(unittest2.TestCase):
    def test_init(self):
        """Initialise a trols_stats.Game object.
        """
        game = trols_stats.Game()
        msg = 'Object is not of type trols_stats.Game'
        self.assertIsInstance(game, trols_stats.Game, msg)

    def test_to_json(self):
        """Convert trols_stats.Game() object to JSON.
        """
        game_id = 'xyz'
        game = trols_stats.Game(game_id)

        received = game.to_json()

        expected = '{"id": "xyz"}'
        msg = 'trols_stats.Game() to JSON error'
        self.assertEqual(received, expected, msg)
