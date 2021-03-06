"""Unit test cases for the :class:`trols_stats.Scraper` class.

"""
import unittest
import os
import lxml

import trols_stats

from trols_stats.tests.results.match_stats import (MATCH_STATS,
                                                   MATCH_STATS_SINGLES,
                                                   DVTA_MATCH_STATS,
                                                   DVTA_TN_MATCH_STATS)


class TestScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

        cls._files_dir = os.path.join('trols_stats', 'tests', 'files')

    def test_init(self):
        """Initialise a trols_stats.Scraper object.
        """
        scraper = trols_stats.Scraper()
        msg = 'Object is not of type trols_stats.Scraper'
        self.assertIsInstance(scraper, trols_stats.Scraper, msg)

    def test_scrape_competition_ids(self):
        """Test scrape_competition_ids.
        """
        # Given a TROLS competition|section results page
        test_file = os.path.join(self._files_dir, 'main_results.php')
        with open(test_file) as html_fh:
            html = html_fh.read()

        # and an xpath definition to target the extraction
        xpath = '//select[@id="section" and @name="section"]/option'

        # when I scrape the page for match competitions
        received = trols_stats.Scraper.scrape_competition_ids(html, xpath)

        # then I should receive a list of match competition codes of the
        # form {'GIRLS 1': 'AA026', 'GIRLS 2': 'AA027', ...}
        expected = {
            'BOYS 1': 'AA001',
            'BOYS 10': 'AA010',
            'BOYS 11': 'AA011',
            'BOYS 12': 'AA012',
            'BOYS 13': 'AA013',
            'BOYS 14': 'AA014',
            'BOYS 15': 'AA015',
            'BOYS 16': 'AA016',
            'BOYS 17': 'AA017',
            'BOYS 18': 'AA018',
            'BOYS 19': 'AA019',
            'BOYS 2': 'AA002',
            'BOYS 20': 'AA020',
            'BOYS 21': 'AA021',
            'BOYS 22': 'AA022',
            'BOYS 23': 'AA023',
            'BOYS 24': 'AA024',
            'BOYS 25': 'AA025',
            'BOYS 3': 'AA003',
            'BOYS 4': 'AA004',
            'BOYS 5': 'AA005',
            'BOYS 6': 'AA006',
            'BOYS 7': 'AA007',
            'BOYS 8': 'AA008',
            'BOYS 9': 'AA009',
            'GIRLS 1': 'AA026',
            'GIRLS 10': 'AA035',
            'GIRLS 11': 'AA036',
            'GIRLS 12': 'AA037',
            'GIRLS 13': 'AA038',
            'GIRLS 14': 'AA039',
            'GIRLS 15': 'AA040',
            'GIRLS 2': 'AA027',
            'GIRLS 3': 'AA028',
            'GIRLS 4': 'AA029',
            'GIRLS 5': 'AA030',
            'GIRLS 6': 'AA031',
            'GIRLS 7': 'AA032',
            'GIRLS 8': 'AA033',
            'GIRLS 9': 'AA034',
        }
        msg = 'Competition IDs extracted error'
        self.assertDictEqual(received, expected, msg)

    def test_get_competition_id(self):
        """Test get_competition_id.
        """
        # Given a NEJTA competition lxml.html.HtmlElement instance
        element = lxml.html.HtmlElement()
        element.attrib['value'] = 'AA026'
        element.text = 'GIRLS 1'

        # when I extract the competition ID
        loader = trols_stats.Scraper()
        received = loader._get_competition_id(element)

        # then I should receive a dictionary structure of the form
        # {'GIRLS 1': 'AA026'}
        expected = {'GIRLS 1': 'AA026'}
        msg = 'Competition dictionary error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_competition_name(self):
        """Scrape_competition name.
        """
        # Given a TROLS competition|section results page
        test_file = os.path.join(self._files_dir, 'main_results.php')
        with open(test_file) as html_fh:
            html = html_fh.read()

        # and an xpath definition to target the extraction
        xpath = '//table/tr/td/select/option[@value="AA"]/text()'

        # when I scrape the page for match competitions
        received = trols_stats.Scraper.scrape_competition_name(html, xpath)

        # then I should receive the competition name
        expected = 'Saturday AM - Autumn 2015'
        msg = 'Competition name extracted error'
        self.assertEqual(received, expected, msg)

    def test_scrape_competition_name_with_league(self):
        """Scrape_competition name: with league.
        """
        # Given a TROLS competition|section results page
        test_file = os.path.join(self._files_dir, 'main_results.php')
        with open(test_file) as html_fh:
            html = html_fh.read()

        # and an xpath definition to target the extraction
        xpath = '//table/tr/td/select/option[@value="AA"]/text()'

        # when I scrape the page for match competitions
        kwargs = {
            'html': html,
            'xpath': xpath,
            'league': 'nejta',
        }
        received = trols_stats.Scraper.scrape_competition_name(**kwargs)

        # then I should receive the competition name
        expected = 'NEJTA Saturday AM - Autumn 2015'
        msg = 'Competition name extracted error'
        self.assertEqual(received, expected, msg)

    def test_scrape_competition_name_tokenised(self):
        """Scrape_competition name: tokenised.
        """
        # Given a TROLS competition|section results page
        test_file = os.path.join(self._files_dir, 'main_results.php')
        with open(test_file) as html_fh:
            html = html_fh.read()

        # and an xpath definition to target the extraction
        xpath = '//table/tr/td/select/option[@value="AA"]/text()'

        # when I scrape the page for match competitions
        kwargs = {
            'html': html,
            'xpath': xpath,
            'tokenise': True,
            'league': 'nejta',
        }
        received = trols_stats.Scraper.scrape_competition_name(**kwargs)

        # then I should receive the competition name
        expected = 'nejta_saturday_am_autumn_2015'
        msg = 'Competition name extracted (tokenised) error'
        self.assertEqual(received, expected, msg)

    def test_scrape_competition_name_with_league_tokenised(self):
        """Scrape_competition name: with league tokenised.
        """
        # Given a TROLS competition|section results page
        test_file = os.path.join(self._files_dir, 'main_results.php')
        with open(test_file) as html_fh:
            html = html_fh.read()

        # and an xpath definition to target the extraction
        xpath = '//table/tr/td/select/option[@value="AA"]/text()'

        # when I scrape the page for match competitions
        received = trols_stats.Scraper.scrape_competition_name(html,
                                                               xpath,
                                                               True)

        # then I should receive the competition name
        expected = 'saturday_am_autumn_2015'
        msg = 'Competition name extracted (tokenised) error'
        self.assertEqual(received, expected, msg)

    def test_scrape_match_ids(self):
        """Test scrape_match_ids.
        """
        # Given a TROLS competition|section results page
        with open(os.path.join(self._files_dir,
                               'www.trols.org.au',
                               'nejta',
                               'results.php')) as _fh:
            html = _fh.read()

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
        match_file = 'nejta_saturday_am_autumn_2015--AA039054.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

        # and an xpath definition to target the team extraction
        xpath = '//table/tr/td/b'

        # when I extract the teams
        received = trols_stats.Scraper.scrape_match_teams(html, xpath)

        # then I should receive a populated dictionary of the form
        # {'home': <home_team>, 'away': <away_team>}
        expected = {'away_team': 'St Marys', 'home_team': 'Watsonia '}
        msg = 'Scraped match detail teams error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_teams_with_color_code(self):
        """Test scrape_match_teams: no color code.
        """
        # Given a TROLS detailed match results page
        match_file = 'nejta_saturday_am_autumn_2015--AA039054.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

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
        expected = {'away_team': 'St Marys', 'home_team': 'Watsonia Red'}
        msg = 'Scraped match detail teams error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_teams_with__late_start(self):
        """Test scrape_match_teams: no color code (late start).
        """
        # Given a TROLS detailed match results page
        match_file = 'match_AA031012.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

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
        expected = {'away_team': 'Eaglemont', 'home_team': 'Clifton'}
        msg = 'Scraped match detail teams error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_teams_with_home_away_color_codes(self):
        """Test scrape_match_teams: home-away color codes.
        """
        # Given a TROLS detailed match results page
        match_file = 'match_AA039094.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

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
        expected = {
            'away_team': 'Watsonia Blue',
            'home_team': 'Watsonia Red'
        }
        msg = 'Scraped match detail teams error (home-away color codes)'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_teams_with_away_only_color_codes(self):
        """Test scrape_match_teams: away only color codes.
        """
        # Given a TROLS detailed match results page
        match_file = 'match_AA039301.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

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
        expected = {
            'away_team': 'Watsonia Blue',
            'home_team': 'Bundoora'
        }
        msg = 'Scraped match detail teams error (home-away color codes)'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_player_names(self):
        """Extract player names from detailed results page.
        """
        # Given a TROLS detailed match results page
        match_file = 'nejta_saturday_am_autumn_2015--AA039054.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

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
        match_file = 'nejta_saturday_am_autumn_2015--AA039054.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

        # and an xpath definition to target the match preamble extraction
        xpath = '//table/tr/td[contains(@class, "mb")]/text()'

        # when I extract the match preamble
        received = trols_stats.Scraper.scrape_match_preamble(html, xpath)

        # then I should receive a dictionary structure of the form
        # {'competition': <girls_or_boys>,
        #  'section': <section_no>,
        #  'date': <date>,
        #  'match_round': <round_no>}
        expected = {'competition_type': 'girls',
                    'section': 14,
                    'date': '28 Feb 15',
                    'match_round': 5}
        msg = 'Match preamble dictionary error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_preamble_dvta_thursday_night(self):
        """Extract match preamble: DVTA Thursday night.
        """
        # Given a TROLS detailed match results page
        match_file = 'match_HN020143.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

        # and an xpath definition to target the match preamble extraction
        xpath = '//table/tr/td[contains(@class, "mb")]/text()'

        # when I extract the match preamble
        received = trols_stats.Scraper.scrape_match_preamble(html, xpath)

        # then I should receive a dictionary structure of the form
        # {'competition': <girls_or_boys>,
        #  'section': <section_no>,
        #  'date': <date>,
        #  'match_round': <round_no>}
        expected = {'competition_type': None,
                    'section': 8,
                    'date': '19 May 16',
                    'match_round': 14}
        msg = 'Match preamble dictionary error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_preamble_dvta_thursday_am(self):
        """Extract match preamble: DVTA Thursday AM.
        """
        # Given a TROLS detailed match results page
        match_file = 'dvta_thursday_am_autumn_2017--HA012053.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

        # and an xpath definition to target the match preamble extraction
        xpath = '//table/tr/td[contains(@class, "mb")]/text()'

        # when I extract the match preamble
        received = trols_stats.Scraper.scrape_match_preamble(html, xpath)

        # then I should receive a dictionary structure of the form
        # {'competition': <girls_or_boys>,
        #  'section': <section_no>,
        #  'date': <date>,
        #  'match_round': <round_no>}
        expected = {'competition_type': None,
                    'section': 4,
                    'date': '2 Mar 17',
                    'match_round': 5}
        msg = 'Match preamble dictionary error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_preamble_semi_final(self):
        """Extract match preamble: semi final.
        """
        # Given a TROLS detailed match results page: semi final
        match_semi_final = 'match_AA039301.html'
        with open(os.path.join(self._files_dir, match_semi_final)) as _fh:
            html = _fh.read()

        # and an xpath definition to target the match preamble extraction
        xpath = '//table/tr/td[contains(@class, "mb")]/text()'

        # when I extract the match preamble
        received = trols_stats.Scraper.scrape_match_preamble(html, xpath)

        # then I should receive a dictionary structure of the form
        # {'competition': <girls_or_boys>,
        #  'section': <section_no>,
        #  'date': <date>,
        #  'match_round': <round_no>}
        expected = {
            'competition_type': 'girls',
            'section': 14,
            'match_round': 'Semi Final'
        }
        msg = 'Match preamble (semi-final) dictionary error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_scores_doubles(self):
        """Scrape match scores: doubles.
        """
        # Given a TROLS detailed match results page
        match_file = 'nejta_saturday_am_autumn_2015--AA039054.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

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

    def test_scrape_match_scores_doubles_dvta_thursday_night(self):
        """Scrape match scores: doubles DVTA Thursday night.
        """
        # Given a TROLS detailed match results page
        match_file = 'match_HN020143.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

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
        expected = DVTA_MATCH_STATS
        msg = 'Match stats dictionary structure error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_scores_doubles_dvta_tuesday_night(self):
        """Scrape match scores: doubles DVTA Tuesday night.
        """
        # Given a TROLS detailed match results page
        match_file = 'match_TN024321.html'
        with open(os.path.join(self._files_dir, match_file)) as _fh:
            html = _fh.read()

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
        expected = DVTA_TN_MATCH_STATS
        msg = 'Match stats dictionary structure error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_scores_singles(self):
        """Scrape match scores: singles.
        """
        # Given a TROLS detailed match results page
        match_singles_file = 'match_AA026044.html'
        with open(os.path.join(self._files_dir,
                               match_singles_file)) as _fh:
            html = _fh.read()

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
        expected = MATCH_STATS_SINGLES
        msg = 'Match stats dictionary (singles) structure error'
        self.assertDictEqual(received, expected, msg)

    def test_scrape_match_scores_dvta_friday_night(self):
        """Scrape match scores: DVTA Friday night.
        """
        # Given a TROLS detailed match results page
        match_singles_file = 'dvta_friday_night_autumn_2017--FN004054.html'
        with open(os.path.join(self._files_dir,
                               match_singles_file)) as _fh:
            html = _fh.read()

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
        expected = {
            1: [
                {
                    'opposition': (6, None),
                    'score_against': 3,
                    'team_mate': None,
                    'score_for': 6
                },
                {
                    'opposition': (5, None),
                    'score_against': 0,
                    'team_mate': None,
                    'score_for': 6
                }
            ],
            2: [
                {
                    'opposition': (5, None),
                    'score_against': 1,
                    'team_mate': None,
                    'score_for': 6
                },
                {
                    'opposition': (6, None),
                    'score_against': 0,
                    'team_mate': None,
                    'score_for': 6
                }
            ],
            3: [
                {
                    'opposition': (8, None),
                    'score_against': 3,
                    'team_mate': None,
                    'score_for': 6
                },
                {
                    'opposition': (7, None),
                    'score_against': 5,
                    'team_mate': None,
                    'score_for': 6
                }
            ],
            4: [
                {
                    'opposition': (7, None),
                    'score_against': 0,
                    'team_mate': None,
                    'score_for': 6
                },
                {
                    'opposition': (8, None),
                    'score_against': 6,
                    'team_mate': None,
                    'score_for': 0
                }
            ],
            5: [
                {
                    'opposition': (2, None),
                    'score_against': 6,
                    'team_mate': None,
                    'score_for': 1
                },
                {
                    'opposition': (1, None),
                    'score_against': 6,
                    'team_mate': None,
                    'score_for': 0
                }
            ],
            6: [
                {
                    'opposition': (1, None),
                    'score_against': 6,
                    'team_mate': None,
                    'score_for': 3
                },
                {
                    'opposition': (2, None),
                    'score_against': 6,
                    'team_mate': None,
                    'score_for': 0
                }
            ],
            7: [
                {
                    'opposition': (4, None),
                    'score_against': 6,
                    'score_for': 0,
                    'team_mate': None
                },
                {
                    'opposition': (3, None),
                    'score_against': 6,
                    'score_for': 5,
                    'team_mate': None
                }
            ],
            8: [
                {
                    'opposition': (3, None),
                    'score_against': 6,
                    'score_for': 3,
                    'team_mate': None
                },
                {
                    'opposition': (4, None),
                    'score_against': 0,
                    'score_for': 6,
                    'team_mate': None
                }
            ]
        }
        msg = 'Match stats dictionary (singles) structure error'
        self.assertDictEqual(received, expected, msg)

    def test_extract_player_codes_singles(self):
        """Extract raw HTML player codes: singles
        """
        # Given a raw segment of HTML representing a player code
        raw_player_code = "1"

        # when I extract the player code
        received = trols_stats.Scraper.extract_player_codes(raw_player_code)

        # then I should receive a tuple construct
        expected = (1, None)
        msg = 'Singles raw HTML parse error'
        self.assertTupleEqual(received, expected, msg)

    def test_extract_player_codes_doubles(self):
        """Extract raw HTML player codes: doubles
        """
        # Given a raw segment of HTML representing a doubles player code
        raw_player_code = "1+4"

        # when I extract the player codes
        received = trols_stats.Scraper.extract_player_codes(raw_player_code)

        # then I should receive a tuple construct
        expected = (1, 4)
        msg = 'Doubles raw HTML parse error'
        self.assertTupleEqual(received, expected, msg)

    def test_create_stat(self):
        """Create a match results stat.
        """
        # Given a tuple of players
        players = ((1, 2), (1, 2))

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
        players = ((1, 2), (1, 2))

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
        players = ((1, 2), (1, 2))

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
        players = ((1, 2), (1, 2))

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

    def test_create_stat_singles(self):
        """Create a match results stat: singles.
        """
        # Given a tuple of players
        players = ((1, None), (1, None))

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players, results)

        # then I should receive a dictionary structure of the form
        expected = {
            'team_mate': None,
            'opposition': (5, None),
            'score_for': 3,
            'score_against': 6,
        }
        msg = 'Match stat creation error'
        self.assertDictEqual(received, expected, msg)

    def test_create_stat_away_singles(self):
        """Create a match results stat: away singles.
        """
        # Given a tuple of players
        players = ((1, None), (1, None))

        # and a tuple of results
        results = (3, 6)

        # when I create an away team stat
        received = trols_stats.Scraper.create_stat(players,
                                                   results,
                                                   away_team=True)

        # then I should receive a dictionary structure of the form
        expected = {
            'team_mate': None,
            'opposition': (1, None),
            'score_for': 6,
            'score_against': 3,
        }
        msg = 'Match stat creation error: away_team singles'
        self.assertDictEqual(received, expected, msg)

    def test_create_stat_reverse_singles(self):
        """Create a match results stat: reverse singles.
        """
        # Given a tuple of players
        players = ((1, None), (1, None))

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players, results, True)

        # then I should receive None
        msg = 'Match stat for reverse singles not None'
        self.assertIsNone(received, msg)

    def test_create_stat_reverse_away_singles(self):
        """Create a match results stat: away team reverse singles.
        """
        # Given a tuple of players
        players = ((1, None), (1, None))

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players,
                                                   results,
                                                   reverse=True,
                                                   away_team=True)

        # then I should receive None
        msg = 'Match stat for away reverse singles not None'
        self.assertIsNone(received, msg)

    def test_create_stat_dvta_singles(self):
        """Create a match results stat: DVTA singles.
        """
        # Given a tuple of players
        players = ((1, None), (2, None))

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players, results)

        # then I should receive a dictionary structure of the form
        expected = {
            'team_mate': None,
            'opposition': (6, None),
            'score_for': 3,
            'score_against': 6,
        }
        msg = 'Match stat creation error'
        self.assertDictEqual(received, expected, msg)

    def test_create_stat_away_dvta_singles(self):
        """Create a match results stat: away DVTA singles.
        """
        # Given a tuple of players
        players = ((1, None), (2, None))

        # and a tuple of results
        results = (3, 6)

        # when I create an away team stat
        received = trols_stats.Scraper.create_stat(players,
                                                   results,
                                                   away_team=True)

        # then I should receive a dictionary structure of the form
        expected = {
            'team_mate': None,
            'opposition': (1, None),
            'score_for': 6,
            'score_against': 3,
        }
        msg = 'Match stat creation error: away_team singles'
        self.assertDictEqual(received, expected, msg)

    def test_create_stat_reverse_dvta_singles(self):
        """Create a match results stat: reverse DVTA singles.
        """
        # Given a tuple of players
        players = ((1, None), (2, None))

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players,
                                                   results,
                                                   reverse=True)

        # then I should receive None
        msg = 'Match stat for reverse DVTA singles not None'
        self.assertIsNone(received, msg)

    def test_create_stat_reverse_away_dvta_singles(self):
        """Create a match results stat: away team reverse singles.
        """
        # Given a tuple of players
        players = ((1, None), (1, None))

        # and a tuple of results
        results = (3, 6)

        # when I create a stat
        received = trols_stats.Scraper.create_stat(players,
                                                   results,
                                                   reverse=True,
                                                   away_team=True)

        # then I should receive None
        msg = 'Match stat for reverse away DVTA singles not None'
        self.assertIsNone(received, msg)

    @classmethod
    def tearDownClass(cls):
        cls._files_dir = None
