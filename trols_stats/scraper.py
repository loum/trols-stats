import lxml.html
import re

from logga.log import log

__all__ = ['Scraper']


class Scraper(object):
    @staticmethod
    def scrape_match_ids(html, xpath):
        """Extract a list of match IDs from *html*.


        During processing, the :mod:`lxml.xpath` extraction will
        produce a list of tuples of the form::

            [('onclick', "open_match(event,'','AA039054');"), ...]

        **Args:**
            *html*: string representation of the HTML page to process.
            *html* is typically a TROLS match results page.

        **Returns:**
            list of match IDs.  For example::

                ['AA039054', <match_id_02>, <match_id_03> ...]

        """
        root = lxml.html.fromstring(html)
        matches = root.xpath(xpath)

        match_ids = []
        for match in matches:
            for attrs in match.items():
                match_id = Scraper.get_match_id(attrs)

                if match_id is None:
                    log.warn('Unable to extract match ID from "%s"' % attrs)
                    continue

                match_ids.append(match_id)

        log.debug('List of match IDs extracted: "%s"' % match_ids)

        return match_ids

    @staticmethod
    def get_match_id(attributes):
        """Extract the TROLS match ID from the results page extraction
        defined by the *attributes* tuple structure.

        **Args:**
            *attributes*: An example of the *attributes* value is::

                ('onclick', "open_match(event,'','AA039054');")

        **Returns:**
            string representation of the match ID.  For example,
            ``AA039054``

        """
        prog = re.compile('open_match\(event,\'\',\'(\w+)\'\);')

        match_id = None
        if attributes[0] == 'onclick':
            re_match = prog.match(attributes[1])
            if re_match:
                match_id = re_match.group(1)
                log.debug('Found match ID: %s' % match_id)

        return match_id

    @staticmethod
    def scrape_match_teams(html, xpath, color_xpath=None):
        """Extract information from the match details *html*.

        **Args:**
            *html*: string representation of the HTML page to process.
            *html* is typically a TROLS detailed match results page.

        **Returns:**
            list of match IDs.  For example::

                ['AA039054', <match_id_02>, <match_id_03> ...]

        """
        def get_team_color_code(root, team, xpath):
            color_xpath = xpath % team
            log.debug('Team color xpath "%s"' % color_xpath)
            color = root.xpath(color_xpath)
            if len(color):
                team += color[0]

            return team

        root = lxml.html.fromstring(html)
        raw_teams = root.xpath(xpath)

        teams = {}
        if len(raw_teams) != 2:
            log.warn('Expecting two teams. Received %d' % len(raw_teams))
        else:
            home_team = raw_teams[0].text
            away_team = raw_teams[1].text

            if color_xpath is not None:
                home_team = get_team_color_code(root,
                                                home_team,
                                                color_xpath)

                away_team = get_team_color_code(root,
                                                away_team,
                                                color_xpath)

            teams['home'] = home_team.replace(u'\xa0', u' ')
            teams['away'] = away_team.replace(u'\xa0', u' ')

        log.debug('Teams extracted: "%s"' % teams)

        return teams

    @staticmethod
    def scrape_player_names(html):
        """Highly customised extract  of player names from *html*.

        **Args:**
            *html*: string representation of the HTML page to process.
            *html* is typically a TROLS match results page.

        **Returns:**
            list of player names.  For example::

                [(1, 'Madeline Doyle'), (2, 'Tara Watson'), ...]

        """
        root = lxml.html.fromstring(html)

        namespaces = {"re": "http://exslt.org/regular-expressions"}
        elements = root.xpath("//td[re:match(text(), '^\d\.')]/text()",
                              namespaces=namespaces)

        player_re = re.compile('^\d\.\s+')
        players = [(i, player_re.sub('', j)) for i, j in enumerate(elements,
                                                                   start=1)]

        log.debug('Players extracted: %s' % players)
        return players
