import urllib
import urllib2
import urlparse
import re
import os
import tempfile

import trols_stats
import trols_stats.interface
from logga.log import log
from filer.files import copy_file

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
    def request(uri, request_args=None, cache_dir=None, force_cache=False):
        """Send a URL request to *uri*.  If *uri* is a file-type resource
        then an attempt will be made to open the file instead.

        **Args:**
            *uri*: the web address to send request

        **Kwargs:**
            *request_args*: dictionary of query terms that will form part
            of the POST request payload

            *cache_dir*: relevant to the TROLS match popups HTML
            response.  Caches the HTML response match popup content
            locally

            *force_cache*: overwrite the file if it already exists in the
            cache

        **Returns:**
            HTML response string of the *uri*

        """
        match_id = None
        if request_args is not None:
            match_id = request_args.get('matchid')

        target_file = None
        if match_id is not None and cache_dir is not None:
            target_file = os.path.join(cache_dir,
                                       'game_{}.html'.format(match_id))
            log.debug('HTML response cache filename: "%s"', target_file)

        html = None
        if (force_cache
                or target_file is None
                or not os.path.exists(target_file)):
            components = urlparse.urlparse(uri)
            log.debug('URI "%s" scheme|path: %s|%s',
                      uri, components.scheme, components.path)
            scheme_match = re.match('http',
                                    components.scheme,
                                    flags=re.IGNORECASE)
            if scheme_match:
                html = Loader._request_url(uri, request_args)
            else:
                html = Loader._request_file(components.path)

        if html is not None:
            if target_file is not None:
                log.info('Writing HTML response to cache file "%s"',
                         target_file)
                with tempfile.NamedTemporaryFile() as _fh:
                    _fh.write(html)
                    _fh.flush()
                    copy_file(_fh.name, target_file)
        else:
            if target_file is not None:
                log.info('Returning HTML response from cache file "%s"',
                         target_file)
                with open(target_file) as _fh:
                    html = _fh.read()

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

        See the :method:`request` method for parameters and return
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
