import urllib2

import trols_stats
import trols_stats.interface
from logga.log import log

__all__ = ['Loader']


class Loader(object):
    """
    .. attribute:: games

    """
    @property
    def games(self):
        return self.__games

    @games.setter
    def games(self, value):
        self.__games = value

    def __init__(self):
        self.__games = []

    def load(self, html):
        """Scrape and load *html* page.

        Produces a list of :class:`trols_stats.model.aggregates.Games`
        objects that are appended to the :attr:`games` attribute.

        **Args:**
            *html*: string representation of the HTML page to process.
            *html* is typically a TROLS match results page.

        """
        # Scrape match teams.
        xpath = '//table/tr/td/b'
        color_xpath = "//table/tr/td/b[contains(text(), '%s')]/span/text()"
        teams = trols_stats.Scraper.scrape_match_teams(html,
                                                       xpath,
                                                       color_xpath)

        # Scrape player names.
        players = trols_stats.Scraper.scrape_player_names(html)

        # Scrape match preamble.
        xpath = '//table/tr/td[contains(@class, "mb")]/text()'
        preamble = trols_stats.Scraper.scrape_match_preamble(html, xpath)

        # Scrape match scores.
        xpath = '//td/table/tr[contains(@valign, "top")]/td'
        match_data = trols_stats.Scraper.scrape_match_scores(html, xpath)

        # Augment the data structures.
        #
        # Fixture needs the teams.
        fixture = preamble.copy()
        fixture.update(teams)
        log.debug('Fixture: %s' % fixture)

        # Build the Game aggregate object.
        stats = trols_stats.Stats(players=dict(players),
                                  teams=teams,
                                  fixture=fixture)
        stats.build_game_aggregate(match_data)
        self.games.extend(stats.games_cache)

    @staticmethod
    def get_main_results_page():
        """Get the main results page.

        This is the NEJTA top level results.php page that contains
        the competition codes.  For example, ``GIRLS 1`` and code ``AA026``.

        """
        request = urllib2.Request('http://trols.org.au/nejta/results.php')

        response = urllib2.urlopen(request)
        html = response.read()

        return html
