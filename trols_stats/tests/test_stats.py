"""Unit test cases for the :class:`trols_stats.Stats` class.

"""
import unittest

import trols_stats
import trols_stats.model
from trols_stats.tests.results.game_aggregates import (DOUBLES,
                                                       COLOR_CODED_DOUBLES,
                                                       COLOR_CODED_4TH_DOUBLES)


class TestStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

    def test_init(self):
        """Initialise a trols_stats.Stats object.
        """
        stats = trols_stats.Stats()
        msg = 'Object is not a trols_stats.Stats'
        self.assertIsInstance(stats, trols_stats.Stats, msg)

    def test_set_players_cache_new_player(self):
        """trols_stats.model.entities.Player cache: new player.
        """
        # Given a scraped player tuple
        player = {'name': 'Madeline Doyle',
                  'team': 'Watsonia Red'}

        # and the player does not exist in the cache
        stats = trols_stats.Stats()

        # when I load the player into the players cache
        received = stats.set_players_cache(player)

        # then I should receive a trols_stats.model.entities.Player object
        msg = 'Stats players cache error: new player'
        self.assertIsInstance(received,
                              trols_stats.model.entities.Player,
                              msg)

    def test_set_fixture_cache_new_fixture(self):
        """trols_stats.model.entities.Fixture cache: new fixture
        """
        # Given a scraped fixture tuple
        fixture = {
            'competition': 'girls',
            'section': 14,
            'date': '28 Feb 15',
            'match_round': 5,
            'home_team': 'Watsonia Red',
            'away_team': 'St Marys',
        }

        # and the fixture does not exist in the cache
        stats = trols_stats.Stats()

        # when I load the fixture into the fixture cache
        received = stats.set_fixtures_cache(fixture)

        # then I should receive a trols_stats.model.entities.Fixture object
        msg = 'Stats fixture cache error: new fixture'
        self.assertIsInstance(received,
                              trols_stats.model.entities.Fixture,
                              msg)

    def test_set_players_cache_existing_player(self):
        """Create a local trols_stats.model.Player() cache: new player.
        """
        # Given a scraped player tuple
        player = {'name': 'Madeline Doyle',
                  'team': 'Watsonia Red'}

        # and the player already exists in the cache
        stats = trols_stats.Stats()
        stats.set_players_cache(player)

        # when I reload the player into the players cache
        received = stats.set_players_cache(player)

        # then I should receive a trols_stats.model.entities.Player() object
        msg = 'Stats players cache error: player create'
        self.assertIsInstance(received,
                              trols_stats.model.entities.Player,
                              msg)

        # and only a single player should exist in the player cache
        received = len(stats.players_cache)
        expected = 1
        msg = 'Length of players_cache should be 1: existing player'
        self.assertEqual(received, expected, msg)

    def test_set_fixture_cache_existing_fixture(self):
        """Create a local trols_stats.model.Player() cache: new fixture
        """
        # Given a scraped fixture tuple
        fixture = {
            'competition_type': 'girls',
            'competition': 'saturday_am_autumn_2015',
            'section': 14,
            'date': '28 Feb 15',
            'match_round': 5,
            'home_team': 'Watsonia Red',
            'away_team': 'St Marys',
        }

        # and the fixture already exists in the cache
        stats = trols_stats.Stats()
        stats.set_fixtures_cache(fixture)

        # when I reload the fixture into the fixtures cache
        received = stats.set_fixtures_cache(fixture)

        # then I should receive a trols_stats.model.entities.Player() object
        msg = 'Stats fixtures cache error: fixture create'
        self.assertIsInstance(received,
                              trols_stats.model.entities.Fixture,
                              msg)

        # and only a single fixture should exist in the fiture cache
        received = len(stats.fixtures_cache)
        expected = 1
        msg = 'Length of fixtures_cache should be 1: existing fixture'
        self.assertEqual(received, expected, msg)

    def test_game_aggregate(self):
        """Create a trols_stats.Game() aggregate object.
        """
        # Given a fixture details data structure
        fixture = {
            'competition_type': 'girls',
            'competition': 'saturday_am_autumn_2015',
            'section': 14,
            'date': '28 Feb 15',
            'match_round': 5,
            'home_team': 'Watsonia Red',
            'away_team': 'St Marys',
        }

        # and a match players data structure
        players = [
            (1, 'Madeline Doyle'),
            (2, 'Tara Watson'),
            (3, 'Alexis McIntosh'),
            (4, 'Grace Heaver'),
            (5, 'Lauren Amsing'),
            (6, 'Mia Bovalino'),
            (7, 'Lucinda Ford'),
            (8, 'Brooke Moore')
        ]

        # and a teams data structure
        teams = {'away_team': 'St Marys', 'home_team': 'Watsonia Red'}

        # and a match stats structure
        stats_data = {
            1: [
                {
                    'opposition': (5, 6),
                    'score_against': 6,
                    'score_for': 3,
                    'player_won': False,
                    'team_mate': 2
                }
            ]
        }

        # when I create the game aggregate
        stats = trols_stats.Stats(players=dict(players),
                                  teams=teams,
                                  fixture=fixture)
        stats.build_game_aggregate(stats_data)

        # then I should receive a Game dictionary object
        received = stats.games_cache[0]()
        expected = DOUBLES
        msg = 'Games aggregate (singles) error'
        self.assertDictEqual(received, expected, msg)

    def test_game_aggregate_color_coded_teams(self):
        """Create a trols_stats.Game() aggregate object.
        """
        # Given a fixture details data structure
        fixture = {
            'competition_type': 'girls',
            'competition': 'saturday_am_autumn_2015',
            'section': 14,
            'date': '18 Apr 15',
            'match_round': 9,
            'home_team': 'Watsonia Red',
            'away_team': 'Watsonia Blue',
        }

        # and a match players data structure
        players = [
            (1, 'Grace Heaver'),
            (2, 'Alexis McIntosh'),
            (3, 'Madeline Doyle'),
            (4, 'Tara Watson'),
            (5, 'Eboni Amos'),
            (6, 'Isabella Markovski'),
            (7, 'Maddison Hollyoak'),
            (8, 'Lily Matt')
        ]

        # and a teams data structure
        teams = {'away_team': 'Watsonia Blue', 'home_team': 'Watsonia Red'}

        # and a match stats structure
        stats_data = {
            1: [
                {
                    'opposition': (5, 6),
                    'score_against': 6,
                    'score_for': 3,
                    'player_won': False,
                    'team_mate': 2
                }
            ]
        }

        # when I create the game aggregate
        stats = trols_stats.Stats(players=dict(players),
                                  teams=teams,
                                  fixture=fixture)
        stats.build_game_aggregate(stats_data)

        # then I should receive a Game dictionary object
        received = stats.games_cache[0]()
        expected = COLOR_CODED_DOUBLES
        msg = 'Games aggregate (singles) error'
        self.assertDictEqual(received, expected, msg)

    def test_game_aggregate_color_coded_teams_fourth_player(self):
        """Create a trols_stats.Game() aggregate object: fourth player.
        """
        # Given a fixture details data structure
        fixture = {
            'competition_type': 'girls',
            'competition': 'saturday_am_autumn_2015',
            'section': 14,
            'date': '7 Feb 15',
            'match_round': 2,
            'home_team': 'Watsonia Blue',
            'away_team': 'Watsonia Red',
        }

        # and a match players data structure
        players = [
            (1, 'Lily Matt'),
            (2, 'Isabella Markovski'),
            (3, 'Maddison Hollyoak'),
            (4, 'Eboni Amos'),
            (5, 'Tara Watson'),
            (6, 'Sallyanne Glover'),
            (7, 'Grace Heaver'),
            (8, 'Madeline Doyle')
        ]

        # and a teams data structure
        teams = {'away_team': 'Watsonia Red', 'home_team': 'Watsonia Blue'}

        # and a match stats structure
        stats_data = {
            2: [
                {
                    'opposition': (6, 8),
                    'score_against': 2,
                    'score_for': 6,
                    'player_won': True,
                    'team_mate': 4
                }
            ]
        }

        # when I create the game aggregate
        stats = trols_stats.Stats(players=dict(players),
                                  teams=teams,
                                  fixture=fixture)
        stats.build_game_aggregate(stats_data)

        # then I should receive a Game dictionary object
        received = stats.games_cache[0]()
        expected = COLOR_CODED_4TH_DOUBLES
        msg = 'Games aggregate (singles) error'
        self.assertDictEqual(received, expected, msg)

    def test_game_aggregate_singles(self):
        """Create a trols_stats.Game() aggregate object: singles.
        """
        # Given a fixture details data structure
        fixture = {
            'competition_type': 'girls',
            'competition': 'saturday_am_autumn_2015',
            'section': 1,
            'date': '21 Feb 15',
            'match_round': 4,
            'home_team': 'Norris Bank',
            'away_team': 'Eltham',
        }

        # and a match players data structure
        players = [
            (1, 'Mladena Mitic'),
            (2, 'Erica Bramble'),
            (3, 'Indiana Pisasale'),
            (4, 'Sasha Pecanic'),
            (5, 'Shania Peric'),
            (6, 'Maddison Batchelor'),
            (7, 'Kristen Fisher'),
            (8, 'Paris Batchelor')
        ]

        # and a teams data structure
        teams = {'away_team': 'Eltham', 'home_team': 'Norris Bank'}

        # and a match stats structure
        stats_data = {
            7: [
                {
                    'opposition': (3, None),
                    'score_against': 3,
                    'score_for': 6,
                    'player_won': True,
                    'team_mate': None
                }
            ]
        }

        # when I create the game aggregate
        stats = trols_stats.Stats(players=dict(players),
                                  teams=teams,
                                  fixture=fixture)
        stats.build_game_aggregate(stats_data)

        # then I should receive a Game dictionary object
        received = stats.games_cache[0]()
        # expected = SINGLES
        expected = {
            'player_won': True,
            'score_against': 3,
            'fixture': {
                'home_team': 'Norris Bank',
                'away_team': 'Eltham',
                'section': 1,
                'competition': 'saturday_am_autumn_2015',
                'competition_type': 'girls',
                'date': '21 Feb 15',
                'match_round': 4
            },
            'score_for': 6,
            'player_won': True,
            'player': {
                'team': 'Eltham',
                'name': 'Kristen Fisher'
            },
            'opposition': [
                {
                    'team': 'Norris Bank',
                    'name': 'Indiana Pisasale'
                }
            ]
        }
        msg = 'Games aggregate (singles) error'
        self.assertDictEqual(received, expected, msg)

    def test_get_oppositon_doubles(self):
        """Get the opposition players (doubles) data structure.
        """
        # Given a match players data structure
        players = [
            (1, 'Madeline Doyle'),
            (2, 'Tara Watson'),
            (3, 'Alexis McIntosh'),
            (4, 'Grace Heaver'),
            (5, 'Lauren Amsing'),
            (6, 'Mia Bovalino'),
            (7, 'Lucinda Ford'),
            (8, 'Brooke Moore')
        ]

        # and a teams data structure
        teams = {'away_team': 'St Marys', 'home_team': 'Watsonia Red'}

        # when I create the opposition players data structure
        stats = trols_stats.Stats(players=dict(players), teams=teams)
        opposition = stats.get_opposition((1, 2))

        # then I should a list with two items
        msg = 'Opponents list length not 2'
        self.assertEqual(len(opposition), 2, msg)

        # and the first opponent should match
        expected = {
            'team': 'Watsonia Red',
            'name': 'Madeline Doyle',
        }
        msg = 'Opposition player structure (doubles 1) incorrect'
        self.assertEqual(opposition[0](), expected, msg)

        # and the second opponent should match
        expected = {
            'team': 'Watsonia Red',
            'name': 'Tara Watson'
        }

    def test_get_oppositon_singles(self):
        """Get the opposition players (singles) data structure.
        """
        # Given a match players data structure
        players = [
            (1, 'Madeline Doyle'),
            (2, 'Tara Watson'),
            (3, 'Alexis McIntosh'),
            (4, 'Grace Heaver'),
            (5, 'Lauren Amsing'),
            (6, 'Mia Bovalino'),
            (7, 'Lucinda Ford'),
            (8, 'Brooke Moore')
        ]

        # and a teams data structure
        teams = {'away_team': 'St Marys', 'home_team': 'Watsonia Red'}

        # when I create the opposition players data structure
        stats = trols_stats.Stats(players=dict(players), teams=teams)
        opposition = stats.get_opposition((1, None))

        # then I should a list with two items
        msg = 'Opponents list length not 2'
        self.assertEqual(len(opposition), 2, msg)

        # and the first opponent should match
        expected = {
            'team': 'Watsonia Red',
            'name': 'Madeline Doyle'
        }
        msg = 'Opposition player structure (singles) incorrect'
        self.assertEqual(opposition[0](), expected, msg)

        # and the second index should be None
        msg = 'Opposition player structure (singles) incorrect'
        self.assertIsNone(opposition[1], msg)
