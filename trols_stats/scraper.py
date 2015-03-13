import lxml.html
import re

from logga.log import log

__all__ = ['Scraper']


class Scraper(object):
    def __init__(self):
        log.debug('Scraper __init__')

    @staticmethod
    def scrape_match_ids(html):
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
        matches = root.xpath('//a[contains(@onclick, "open_match")]')

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