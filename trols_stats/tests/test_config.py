import unittest2
import os

import trols_stats


class TestConfig(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__test_dir = os.path.join('trols_stats', 'tests', 'files')
        cls.__conf_path = os.path.join(cls.__test_dir, 'config.conf')

    def test_init(self):
        """Initialise a TrolsStatsConfig object.
        """
        conf = trols_stats.Config()
        msg = 'Object is not a trols_stats.Config'
        self.assertIsInstance(conf, trols_stats.Config, msg)

    def test_parse_config_main_results(self):
        """Parse main_results from the config.
        """
        # Given a TROLS Stats config instance
        conf = trols_stats.Config(self.__conf_path)

        # when I reference the main_results attribute
        received = conf.main_results

        # then I should get the expected URL
        expected = 'http://trols.org.au/nejta/results.php'
        msg = 'trols_stats.Config.main_results error'
        self.assertEqual(received, expected, msg)

    def test_parse_config_cache_dir(self):
        """Parse cache_dir from the config.
        """
        # Given a TROLS Stats config instance
        conf = trols_stats.Config(self.__conf_path)

        # when I reference the cache_dir attribute
        received = conf.cache_dir

        # then I should get the expected directory
        expected = os.path.join(os.sep, 'tmp', 'trols_stats')
        msg = 'trols_stats.Config.cache_dir error'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls.__test_dir = None
        cls.__conf_path = None
