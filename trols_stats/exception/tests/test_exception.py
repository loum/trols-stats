import unittest2

import trols_stats.exception


class TestTrolsStatsConfigError(unittest2.TestCase):

    def test_error_code_1000(self):
        """Config file not found: code 1000.
        """
        try:
            raise trols_stats.exception.TrolsStatsConfigError(1000)
        except trols_stats.exception.TrolsStatsConfigError as received:
            expected = '1000: Config file not found'
            msg = 'TestTrolsStatsConfigError code 1000: error'
            self.assertEqual(str(received), expected, msg)

    def test_error_code_1001(self):
        """No config elements have been found: code 1001.
        """
        try:
            raise trols_stats.exception.TrolsStatsConfigError(1001)
        except trols_stats.exception.TrolsStatsConfigError as received:
            expected = '1001: No config elements have been defined'
            msg = 'TestTrolsStatsConfigError code 1001: error'
            self.assertEqual(str(received), expected, msg)
