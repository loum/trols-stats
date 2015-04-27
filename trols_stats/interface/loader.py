import urllib
import urllib2
import urlparse
import re
import json

import trols_stats
import trols_stats.interface
from logga.log import log

__all__ = ['Loader']


class Loader(object):
    """
    .. attribute:: games

    """
    @property
    def competition_map(self):
        return self.__competition_map

    @competition_map.setter
    def competition_map(self, value):
        self.__competition_map.clear()
        self.__competition_map = value

    @property
    def games(self):
        return self.__games

    @games.setter
    def games(self, value):
        self.__games = value

    def __init__(self):
        self.__competition_map = {}
        self.__games = []

    def build_game_map(self, html):
        """Scrape *html* game page and build a game map.

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
    def request(uri, request_args=None):
        """Send a URL request to *uri*.  If *uri* is a file-type resource
        then an attempt will be made to open the file instead.

        **Args:**
            *uri*: the web address to send request

            *request_args*: dictionary of query terms that will put in the
            POST request body

        **Returns:**
            HTML response string of the *uri*

        """
        components = urlparse.urlparse(uri)
        log.debug('scheme|path: %s|%s' %
                  (components.scheme, components.path))

        scheme_match = re.match('http',
                                components.scheme,
                                flags=re.IGNORECASE)
        html = None
        if scheme_match:
            html = Loader._request_url(uri, request_args)
        else:
            html = Loader._request_file(components.path)

        return html

    @staticmethod
    def _request_file(path):
        """Request a file resource.

        .. note:

            Based on the current URI specification as of 2009, RFC 3986,
            ``file`` type schemes cannot represent relative paths.  Here,
            we assume relativeness and reconstruct the path component
            to be relative to the current directory.

        **Args:**
            *path*: file resource as taken from the ``file`` URI scheme type

        **Returns:**
            HTML response string of the *path*

        """
        log.info('Attempting to read file resource "%s"' % path)
        html = None

        with open(path) as file_h:
            html = file_h.read()

        return html

    @staticmethod
    def _request_url(url, request_args=None):
        """Request a URL.

        See the :method:`request_uri` method for parameters and return
        value.

        """
        log.info('Attempting to read URL "%s": args "%s"' %
                 (url, request_args))
        request = urllib2.Request(url)

        if request_args is None:
            request_args = {}

        encoded_args = urllib.urlencode(request_args)

        response = urllib2.urlopen(request, encoded_args)
        html = response.read()

        return html
