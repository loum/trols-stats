import unittest2
import os

import trols_stats.model.aggregates


class TestGame(unittest2.TestCase):
    def test_init(self):
        """Initialise a trols_stats.model.aggregates.Game object.
        """
        game = trols_stats.model.aggregates.Game()
        msg = 'Object is not of type trols_stats.model.aggregates.Game'
        self.assertIsInstance(game, trols_stats.model.aggregates.Game, msg)

    def test_to_json(self):
        """Convert trols_stats.model.aggregates.Game() object to JSON.
        """
        # Given a game data structure
        game_data = {
            'uid': 'xyz'
        }

        # when I create trols_stats.model.aggregate.Game object
        game = trols_stats.model.aggregates.Game(**game_data)

        # and dump to JSON
        received = game.to_json()

        # then I should get a serialised JSON string
        expected_fh = open(os.path.join('trols_stats',
                                        'model',
                                        'aggregates',
                                        'tests',
                                        'results',
                                        'game_aggregate.json'))
        expected = expected_fh.read().rstrip()
        expected_fh.close()
        msg = 'trols_stats.model.Game() to JSON error'
        self.assertEqual(received, expected, msg)
