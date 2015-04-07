import unittest2

import trols_stats.model.entities


class TestPlayer(unittest2.TestCase):
    def test_init(self):
        """Initialise a trols_stats.model.entities.Player object.
        """
        player = trols_stats.model.entities.Player()
        msg = 'Object is not of type trols_stats.model.entities.Player'
        self.assertIsInstance(player,
                              trols_stats.model.entities.Player,
                              msg)

    def test_to_json(self):
        """Convert trols_stats.model.entities.Player() object to JSON.
        """
        # Given a player data structure
        player_data = {
            'uid': 'xyz',
            'name': 'Player 1'
        }

        # when I create a trols_stats.model.entities.Player object
        player = trols_stats.model.entities.Player(**player_data)

        # and dump to JSON
        received = player.to_json()

        # then I should received a serialised JSON string
        expected = '{"uid": "xyz", "name": "Player 1"}'
        msg = 'trols_stats.model.entities.Player() to JSON error'
        self.assertEqual(received, expected, msg)
