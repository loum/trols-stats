"""Unit test cases for the :class:`trols_stats.Config` class.

"""
import unittest
import os

import trols_stats


class TestConfig(unittest.TestCase):
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

    def test_parse_config_trols_urls(self):
        """Parse leagues from the config.
        """
        # Given a TROLS Stats config instance
        conf = trols_stats.Config(self.__conf_path)

        # when I reference the leagues attribute
        received = conf.trols_urls

        # then I should get the expected URL
        expected = {
            'nejta': 'AA',
            'dvta': 'TN,HN',
        }
        msg = 'trols_stats.Config.trols_urls error'
        self.assertEqual(received, expected, msg)

    def test_parse_config_cache(self):
        """Parse cache from the config.
        """
        # Given a TROLS Stats config instance
        conf = trols_stats.Config(self.__conf_path)

        # when I reference the cache attribute
        received = conf.cache

        # then I should get the expected directory
        expected = os.path.join(os.sep, 'tmp', 'trols_stats')
        msg = 'trols_stats.Config.cache error'
        self.assertEqual(received, expected, msg)

    def test_parse_config_shelve(self):
        """Parse shelve from the config.
        """
        # Given a TROLS Stats config instance
        conf = trols_stats.Config(self.__conf_path)

        # when I reference the shelve attribute
        received = conf.shelve

        # then I should get the expected directory
        expected = os.path.join(os.sep, 'tmp', 'trols_shelve')
        msg = 'trols_stats.Config.shelve error'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls.__test_dir = None
        cls.__conf_path = None
