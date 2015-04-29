import unittest2

import trols_stats
import trols_stats.model


class TestStats(unittest2.TestCase):

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
            'competition': 'girls',
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
            'competition': 'girls',
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
        teams = {'away': 'St Marys', 'home': 'Watsonia Red'}

        # and a match stats structure
        stats_data = {
            1: [
                {
                    'opposition': (5, 6),
                    'score_against': 6,
                    'score_for': 3,
                    'team_mate': 2
                }
            ]
        }

        # when I create the game aggregate
        stats = trols_stats.Stats(players=dict(players),
                                  teams=teams,
                                  fixture=fixture)
        stats.build_game_aggregate(stats_data)

        # then I should receive a game object
        received = stats.games_cache
        msg = 'Games aggregate not created'
        self.assertIsInstance(received[0],
                              trols_stats.model.aggregates.Game,
                              msg)
