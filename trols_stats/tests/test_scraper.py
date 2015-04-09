import unittest2
import os

import trols_stats

from trols_stats.tests.results.match_stats import MATCH_STATS


class TestScraper(unittest2.TestCase):
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

        # and an xpath definition to target the extraction
        xpath = '//a[contains(@onclick, "open_match")]'

        # when I scrape the page for match_ids
        received = trols_stats.Scraper.scrape_match_ids(html, xpath)

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

    def test_scrape_match_teams_no_color_code(self):
        """Test scrape_match_teams: no color code.
        """
        # Given a TROLS detailed match results page
        html = self._detailed_results_html

        # and an xpath definition to target the team extraction
        xpath = '//table/tr/td/b'

        # when I extract the teams
        received = trols_stats.Scraper.scrape_match_teams(html, xpath)

        # then I should receive a populated dictionary of the form
        # {'home': <home_team>, 'away': <away_team>}
        expected = {'away': 'St Marys', 'home': 'Watsonia '}
        msg = 'Scraped match detail teams error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_teams_with_color_code(self):
        """Test scrape_match_teams: no color code.
        """
        # Given a TROLS detailed match results page
        html = self._detailed_results_html

        # and an xpath definition to target the team extraction
        xpath = '//table/tr/td/b'

        # and a color xpath definition has been supplied
        color_xpath = "//table/tr/td/b[contains(text(), '%s')]/span/text()"

        # when I extract the teams
        received = trols_stats.Scraper.scrape_match_teams(html,
                                                          xpath,
                                                          color_xpath)

        # then I should receive a populated dictionary of the form
        # {'home': <home_team>, 'away': <away_team>}
        expected = {'away': 'St Marys', 'home': 'Watsonia Red'}
        msg = 'Scraped match detail teams error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_player_names(self):
        """Extract player names from detailed results page.
        """
        # Given a TROLS detailed match results page
        html = self._detailed_results_html

        # when I extract the player names
        received = trols_stats.Scraper.scrape_player_names(html)

        # then I should receive an enumerated type of the form
        # (1: <player_1>, 2: <player_2>, ...)
        expected = [
            (1, 'Madeline Doyle'),
            (2, 'Tara Watson'),
            (3, 'Alexis McIntosh'),
            (4, 'Grace Heaver'),
            (5, 'Lauren Amsing'),
            (6, 'Mia Bovalino'),
            (7, 'Lucinda Ford'),
            (8, 'Brooke Moore')
        ]
        msg = 'Player extraction from match details error'
        self.assertListEqual(received, expected, msg)

    def test_scrape_match_preamble(self):
        """Extract match preamble.
        """
        # Given a TROLS detailed match results page
        html = self._detailed_results_html

        # and an xpath definition to target the match preamble extraction
        xpath = '//table/tr/td[contains(@class, "mb")]/text()'

        # when I extract the match preamble
        received = trols_stats.Scraper.scrape_match_preamble(html, xpath)

        # then I should receive a dictionary structure of the form
        # {'competition': <girls_or_boys>,
        #  'section': <section_no>,
        #  'date': <date>,
        #  'match_round': <round_no>}
        expected = {'competition': 'girls',
                    'section': 14,
                    'date': '28 Feb 15',
                    'match_round': 5}
        msg = 'Match preamble dictionary error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_scores(self):
        """Scrape match scores.
        """
        # Given a TROLS detailed match results page
        html = self._detailed_results_html

        # and an xpath definition to target the match scores extraction
        xpath = '//td/table/tr[contains(@valign, "top")]/td'

        # when I extract the match scores
        received = trols_stats.Scraper.scrape_match_scores(html, xpath)

        # then I should received a dictionary structure of the form
        # {
        #     1: [
        #         {
        #             'opposition': (5, 6),
        #             'score_against': 6,
        #             'score_for': 3,
        #             'team_mate': 2
        #         },
        #     ...
        # }
        expected = MATCH_STATS
        msg = 'Match stats dictionary structure error'
        self.assertDictEqual(received, expected, msg)

    def test_create_stat(self):
        """Create a match results stat.
        """
        # Given a tuple of players
        players = (1, 2)

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players, results)

        # then I should receive a dictionary structure of the form
        expected = {
            'team_mate': 2,
            'opposition': (5, 6),
            'score_for': 3,
            'score_against': 6,
        }
        msg = 'Match stat creation error'
        self.assertDictEqual(received, expected, msg)

    def test_create_stat_away(self):
        """Create a match results stat: away.
        """
        # Given a tuple of players
        players = (1, 2)

        # and a tuple of results
        results = (3, 6)

        # when I create an away team stat
        received = trols_stats.Scraper.create_stat(players,
                                                   results,
                                                   away_team=True)

        # then I should receive a dictionary structure of the form
        expected = {
            'team_mate': 6,
            'opposition': (1, 2),
            'score_for': 6,
            'score_against': 3,
        }
        msg = 'Match stat creation error: away_team'
        self.assertDictEqual(received, expected, msg)

    def test_create_stat_reverse(self):
        """Create a match results stat: reverse.
        """
        # Given a tuple of players
        players = (1, 2)

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players, results, True)

        # then I should receive a dictionary structure of the form
        expected = {
            'team_mate': 1,
            'opposition': (5, 6),
            'score_for': 3,
            'score_against': 6,
        }
        msg = 'Match stat creation error: reverse'
        self.assertDictEqual(received, expected, msg)

    def test_create_stat_reverse_away(self):
        """Create a match results stat: away team reverse.
        """
        # Given a tuple of players
        players = (1, 2)

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players,
                                                   results,
                                                   reverse=True,
                                                   away_team=True)

        # then I should receive a dictionary structure of the form
        expected = {
            'team_mate': 5,
            'opposition': (1, 2),
            'score_for': 6,
            'score_against': 3,
        }
        msg = 'Match stat creation error: away team reverse'
        self.assertDictEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._detailed_results_html = None
