import unittest2

import trols_stats
import trols_stats.model


class TestLoader(unittest2.TestCase):

    def test_init(self):
        """Initialise a trols_stats.Loader object.
        """
        loader = trols_stats.Loader()
        msg = 'Object is not a trols_stats.Loader'
        self.assertIsInstance(loader, trols_stats.Loader, msg)

    def test_set_players_cache_new_player(self):
        """Create a local trols_stats.model.entities.Player cache: new player.
        """
        # Given a scraped player tuple
        player = {'name': 'Madeline Doyle',
                  'team': 'Watsonia Red'}

        # and the player does not exist in the cache
        loader = trols_stats.Loader()

        # when I load the player into the players cache
        received = loader.set_players_cache(player)

        # then I should receive a trols_stats.model.entities.Player object
        msg = 'Loader players cache error: new player'
        self.assertIsInstance(received,
                              trols_stats.model.entities.Player,
                              msg)

    def test_set_players_cache_existing_player(self):
        """Create a local trols_stats.model.Player() cache: new player.
        """
        # Given a scraped player tuple
        player = {'name': 'Madeline Doyle',
                  'team': 'Watsonia Red'}

        # and the player already exists in the cache
        loader = trols_stats.Loader()
        loader.set_players_cache(player)

        # when I reload the player into the players cache
        received = loader.set_players_cache(player)

        # then I should receive a trols_stats.model.entities.Player() object
        msg = 'Loader players cache error: player create'
        self.assertIsInstance(received,
                              trols_stats.model.entities.Player,
                              msg)

        # and only a single player should exist in the player cache
        received = len(loader.players_cache)
        expected = 1
        msg = 'Length of players_cache should be 1: existing player'
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
            'home': 'Watsonia Red',
            'away': 'St Marys',
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
        stats = {
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
        loader = trols_stats.Loader(players=dict(players),
                                    teams=teams,
                                    fixture=fixture)
        loader.build_game_aggregate(stats)

        # then I should receive a game object
        received = loader.games_cache
        msg = 'Games aggregate not created'
        self.assertIsInstance(received[0],
                              trols_stats.model.aggregates.Game,
                              msg)
