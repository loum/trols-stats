"""Unit test cases for the :class:`trols_stats.Statistics` class.

"""
import unittest
import json
import os

import trols_stats
import trols_stats.model.aggregates


class TestStatistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._files_dir = os.path.join('trols_stats', 'tests', 'files')

    def test_init(self):
        """Initialise a trols_stats.Statistics object.
        """
        statistics = trols_stats.Statistics()
        msg = 'Object is not a trols_stats.Statistics'
        self.assertIsInstance(statistics, trols_stats.Statistics, msg)

    def test_aggregate(self):
        """Aggregate results from a list of games.
        """
        # Given a list of games
        with open(os.path.join(self._files_dir,
                               'ise_game_aggregates.json')) as _fh:
            games_json = _fh.read()
        games_raw = json.loads(games_json)
        games = [trols_stats.model.aggregates.Game(**x) for x in games_raw]

        # when I aggregate the game results
        statistics = trols_stats.Statistics()
        for game in games:
            statistics.aggregate(game)

        # then I should get a statistics data structure
        received = statistics()
        expected = {
            'games_lost': 8,
            'games_played': 22,
            'games_won': 14,
            'percentage': 152.7027027027027,
            'score_against': 74,
            'score_for': 113
        }
        msg = 'Player aggregate statistics error'
        self.assertDictEqual(received, expected, msg)
