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
            'name': 'Player 1',
            'team': 'Best Team'
        }

        # when I create a trols_stats.model.entities.Player object
        player = trols_stats.model.entities.Player(**player_data)

        # and dump to JSON
        received = player.to_json()

        # then I should received a serialised JSON string
        expected = '{"team": "Best Team", "uid": "xyz", "name": "Player 1"}'
        msg = 'trols_stats.model.entities.Player() to JSON error'
        self.assertEqual(received, expected, msg)

    def test_equality_dict_base(self):
        """trols_stats.model.entities.Player equality: dict base.
        """
        # Given a player data structure
        player_data = {
            'uid': 'xyz',
            'name': 'Player 1',
            'team': 'Best Team'
        }

        # when I create a trols_stats.model.entities.Player object
        player = trols_stats.model.entities.Player(**player_data)

        # and compare it to a like valued dictionary
        received = (player == {'name': 'Player 1', 'team': 'Best Team'})

        # then comparison should return True
        msg = 'Player dict comparison should return True'
        self.assertTrue(received, msg)

    def test_non_equality_dict_base(self):
        """trols_stats.model.entities.Player non equality: dict base.
        """
        # Given a player data structure
        player_data = {
            'uid': 'xyz',
            'name': 'Player 1',
            'team': 'Best Team'
        }

        # when I create a trols_stats.model.entities.Player object
        player = trols_stats.model.entities.Player(**player_data)

        # and compare it to a different dictionary
        received = (player == {'name': 'Player 1', 'team': 'Worst Team'})

        # then comparison should return False
        msg = 'Player dict comparison should return False'
        self.assertFalse(received, msg)

    def test_equality_obj_base(self):
        """trols_stats.model.entities.Player equality: object base.
        """
        # Given a player data structure
        player_data = {
            'uid': 'xyz',
            'name': 'Player 1',
            'team': 'Best Team'
        }

        # when I create a trols_stats.model.entities.Player object
        player = trols_stats.model.entities.Player(**player_data)

        # and compare it to a like valued Player object
        player_2 = trols_stats.model.entities.Player(**player_data)
        received = (player == player_2)

        # then comparison should return True
        msg = 'Player object comparison should return True'
        self.assertTrue(received, msg)

    def test_non_equality_obj_base(self):
        """trols_stats.model.entities.Player non equality: object base.
        """
        # Given a player data structure
        player_data = {
            'uid': 'xyz',
            'name': 'Player 1',
            'team': 'Best Team'
        }

        # when I create a trols_stats.model.entities.Player object
        player = trols_stats.model.entities.Player(**player_data)

        # and compare it to a unlike Player object
        player_data_2 = {
            'uid': 'abc',
            'name': 'Player 1',
            'team': 'Best Team'
        }
        player_2 = trols_stats.model.entities.Player(**player_data_2)
        received = (player == player_2)

        # then comparison should return False
        msg = 'Player object comparison should return False'
        self.assertFalse(received, msg)
