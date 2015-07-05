import unittest2
import os
import json

import trols_stats.model.entities as entities
import trols_stats.model.aggregates
import trols_stats.model.tests.files.game_aggregates as game_aggregates


class TestGame(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__files_dir = os.path.join('trols_stats',
                                       'model',
                                       'aggregates',
                                       'tests',
                                       'files')
        cls.__results_dir = os.path.join('trols_stats',
                                         'model',
                                         'aggregates',
                                         'tests',
                                         'results')

    def test_init(self):
        """Initialise a trols_stats.model.aggregates.Game object.
        """
        game = trols_stats.model.aggregates.Game()
        msg = 'Object is not of type trols_stats.model.aggregates.Game'
        self.assertIsInstance(game, trols_stats.model.aggregates.Game, msg)

    def test_to_json_doubles(self):
        """Convert aggregates.Game() object to JSON: doubles.
        """
        # Given a game data structure
        game_data = game_aggregates.DOUBLES

        # when I create trols_stats.model.aggregate.Game object
        game = trols_stats.model.aggregates.Game(**game_data)

        # and dump to JSON
        received = game.to_json()

        # then I should get a serialised JSON string
        expected_fh = open(os.path.join(self.__results_dir,
                                        'game_aggregate_doubles.json'))
        expected = expected_fh.read().rstrip()
        expected_fh.close()
        msg = 'trols_stats.model.Game() to JSON error: doubles'
        self.assertEqual(received, expected, msg)

    def test_to_json_singles(self):
        """Convert aggregates.Game() object to JSON: singles.
        """
        # Given a game data structure
        game_data = game_aggregates.SINGLES

        # when I create trols_stats.model.aggregate.Game object
        game = trols_stats.model.aggregates.Game(**game_data)

        # and dump to JSON
        received = game.to_json()

        # then I should get a serialised JSON string
        expected_fh = open(os.path.join(self.__results_dir,
                                        'game_aggregate_singles.json'))
        expected = expected_fh.read().rstrip()
        expected_fh.close()
        msg = 'trols_stats.model.Game() to JSON error: singles'
        self.assertEqual(received, expected, msg)

    def test_build_opposition_singles(self):
        """Build opposition data structure from dictionary source: singles.
        """
        # Given a single player dictionary.
        player = (
            {
                'name': 'Isabella Markovski',
                'team': 'Watsonia',
            },
        )
        # when I build the opposition
        game = trols_stats.model.aggregates.Game()
        game.opposition = player

        # then I should received a tuple with a
        # trols_stats.models.entities.Player item
        players = game.opposition
        received = all(isinstance(oppn,
                                  entities.Player) for oppn in players)
        msg = 'Building opposition structure (single) not a Player object'
        self.assertTrue(received, msg)

        # and the tuple should contain one item
        msg = 'Opposition structure not one item'
        self.assertTrue(len(game.opposition) == 1, msg)

    def test_build_opposition_doubles(self):
        """Build opposition data structure from dictionary source: doubles.
        """
        # Given a doubles player dictionary.
        players = (
            {
                'name': 'Isabella Markovski',
                'team': 'Watsonia',
            },
            {
                'name': 'Eboni Amos',
                'team': 'Watsonia',
            }
        )

        # when I build the opposition
        game = trols_stats.model.aggregates.Game()
        game.opposition = players

        # then I should received a tuple with a
        # trols_stats.models.entities.Player item
        players = game.opposition
        received = all(isinstance(oppn,
                                  entities.Player) for oppn in players)
        msg = 'Building opposition structure (single) not a Player object'
        self.assertTrue(received, msg)

        # and the tuple should contain one item
        msg = 'Opposition structure not one item'
        self.assertTrue(len(game.opposition) == 2, msg)

    def test_player_equals(self):
        """Match Game aggregate subset based on player instance.
        """
        # Given a Game instance
        with open(os.path.join(self.__files_dir,
                               'ise_home_st_marys.json')) as _fh:
            game_source = json.loads(_fh.read())
        game = trols_stats.model.aggregates.Game(**game_source)

        # and a player instance
        player = {
            'section': 14,
            'name': u'Isabella Markovski',
            'team': u'Watsonia Blue'
        }

        # when I compare the game against a player instance
        received = (game == player)

        # then I should get a match
        msg = 'Player instance not matched in Game aggregate'
        self.assertTrue(received, msg)

    def test_player_equals_no_match(self):
        """Match Game aggregate subset based on player instance: no match.
        """
        # Given a Game instance
        with open(os.path.join(self.__files_dir,
                               'ise_home_st_marys.json')) as _fh:
            game_source = json.loads(_fh.read())
        game = trols_stats.model.aggregates.Game(**game_source)

        # and an unmatched player instance
        player = {
            'section': 14,
            'name': u'Eboni Amos',
            'team': u'Watsonia Blue'
        }

        # when I compare the game against a player instance
        received = (game == player)

        # then I should get a match
        msg = 'Player instance should not match Game aggregate'
        self.assertFalse(received, msg)

    @classmethod
    def tearDownClass(cls):
        cls.__files_dir = None
        cls.__results_dir = None
