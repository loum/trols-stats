import unittest2
import os

import trols_stats.interface


class TestLoader(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        test_files_dir = os.path.join('trols_stats',
                                      'tests',
                                      'files',
                                      'www.trols.org.au',
                                      'nejta')
        detailed_results_page = 'match_popup.php?matchid=AA039054.html'

        html_fh = open(os.path.join(test_files_dir, detailed_results_page))
        cls._detailed_results_html = html_fh.read()
        html_fh.close()

    def test_init(self):
        """Initialise a trols_stats.interface.Loader object.
        """
        loader = trols_stats.interface.Loader()
        msg = 'Object is not a trols_stats.interface.Loader'
        self.assertIsInstance(loader, trols_stats.interface.Loader, msg)

    def test_load(self):
        """Scrape and load.
        """
        # Given a TROLS detailed match results page
        html = self._detailed_results_html

        # when a scrape and load occurs
        loader = trols_stats.interface.Loader()
        loader.load(html)
        received = loader.games

        # then I should receive a list of Game objects
        expected = 16
        msg = 'trols_stats.interface.Loader.games list length should be 8'
        self.assertEqual(len(received), expected, msg)

    @classmethod
    def teatDownClass(cls):
        cls._detailed_results_html = None
