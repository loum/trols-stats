import unittest2
import os

import trols_stats


class TestScraper(unittest2.TestCase):
    def test_init(self):
        """Initialise a trols_stats.Scraper object.
        """
        scraper = trols_stats.Scraper()
        msg = 'Object is not of type trols_stats.Scraper'
        self.assertIsInstance(scraper, trols_stats.Scraper, msg)

    def test_scrape_match_ids(self):
        """Test scrape_match_ids.
        """
        # Given a TROLS competition|section results page
        html_fh = open(os.path.join('trols_stats',
                                    'tests',
                                    'files',
                                    'www.trols.org.au',
                                    'nejta',
                                    'results.php'))
        html = html_fh.read()
        html_fh.close()

        # when I scrape the page for match_ids
        scraper = trols_stats.Scraper()
        received = scraper.scrape_match_ids(html)

        # then I should receive a list of match IDs
        expected = ['AA039011',
                    'AA039013',
                    'AA039014',
                    'AA039022',
                    'AA039023',
                    'AA039024',
                    'AA039042',
                    'AA039043',
                    'AA039044',
                    'AA039051',
                    'AA039054']
        msg = 'List of scraped match IDs error'
        self.assertListEqual(sorted(received), sorted(expected), msg)

    def test_get_match_id(self):
        """Test get_match_id.
        """
        # Given a list of TROLS match tuples
        match_attributes = ('onclick',
                            "open_match(event,'','AA039054');")

        # when I attempt to extract the match_ids
        received = trols_stats.Scraper.get_match_id(match_attributes)

        # then I should receive a list of match_ids
        expected = 'AA039054'
        msg = 'Match ID extraction error'
        self.assertEqual(received, expected, msg)
