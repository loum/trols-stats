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
        """Highly customised extract of player names from *html*.

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

    @staticmethod
    def scrape_match_preamble(html, xpath):
        """Extract match preamble from *html*.

        A typical preamble string is as follows::

            GIRLS 14 on 28th Feb 15  Rd.5

        **Args:**
            *html*: string representation of the HTML page to process.
            *html* is typically a TROLS match results page.

        **Returns:**
            dictionary structure representing components of the
            preamble in the form::

                {'sex': <girls_or_boys>,
                 'section': <section_no>,
                 'date': <date>,
                 'round': <round_no>}

        """
        root = lxml.html.fromstring(html)
        preamble = root.xpath(xpath)[0]
        raw_preamble = preamble.replace(u'\xa0', u' ')

        log.debug('Scraped preamble: "%s"' % raw_preamble)

        preamble = {}

        def sex(matchobj):
            match_sex = matchobj.group(1).lower()
            log.debug('Match sex: "%s"' % match_sex)
            preamble['sex'] = match_sex.encode('utf8')

            return matchobj.group(2)

        sex_re = re.compile(r'^(girls|boys)\s+(.*)', re.IGNORECASE)
        raw_preamble = sex_re.sub(sex, raw_preamble)

        def section(matchobj):
            match_section = int(matchobj.group(1))
            log.debug('Match section: %d' % match_section)
            preamble['section'] = match_section

            return matchobj.group(2)

        section_re = re.compile(r'^(\d+)\s+on\s+(.*)')
        raw_preamble = section_re.sub(section, raw_preamble)

        def date(matchobj):
            match_date = ('%s %s %s' % (matchobj.group(1),
                                        matchobj.group(3),
                                        matchobj.group(4)))
            log.debug('Match date: %s' % match_date)
            preamble['date'] = match_date

            return matchobj.group(5)

        date_re = re.compile(r'^(\d+)(st|nd|rd|th)\s+(\w+)\s+(\d{2})\s+(.*)')
        raw_preamble = date_re.sub(date, raw_preamble)

        def round_no(matchobj):
            match_round_no = int(matchobj.group(1))
            log.debug('Match round: %d' % match_round_no)
            preamble['round'] = match_round_no

            return matchobj.group(2)

        round_no_re = re.compile(r'^Rd.(\d+)(.*)')
        raw_preamble = round_no_re.sub(round_no, raw_preamble)

        if len(raw_preamble):
            log.warn('Match preamble string has unparsed tokens "%s"' %
                     raw_preamble)

        return preamble

    @staticmethod
    def scrape_match_scores(html, xpath):
        """Extract match scores from *html*.

        **Args:**
            *html*: string representation of the HTML page to process.
            *html* is typically a TROLS match results page.

        **Returns:**
            dictionary structure representing components of the
            preamble in the form::

        """
        root = lxml.html.fromstring(html)
        raw_scores = root.xpath(xpath)

        count = -1
        active_players = ()
        match_results = {}
        for score in raw_scores:
            count += 1
            if count % 3 == 2:
                continue

            log.debug('score: %s' % score.text)

            player_re = re.compile(r'^(\d+)\+(\d+)')
            players = player_re.match(score.text)
            if players:
                active_players = (int(players.group(1)),
                                  int(players.group(2)))
                log.debug('Players: %s' % (active_players,))
                continue

            score_re = re.compile(r'^(\d+)\-(\d+)')
            scores = score_re.match(score.text)
            if scores:
                active_scores = (int(scores.group(1)),
                                 int(scores.group(2)))
                log.debug('Scores: %s' % (active_scores, ))

                if match_results.get(active_players[0]) is None:
                    match_results[active_players[0]] = []

                stat = Scraper.create_stat(active_players, active_scores)
                match_results[active_players[0]].append(stat)

                if match_results.get(active_players[1]) is None:
                    match_results[active_players[1]] = []

                stat = Scraper.create_stat(active_players,
                                           active_scores,
                                           reverse=True)
                match_results[active_players[1]].append(stat)

                if match_results.get(active_players[0] + 4) is None:
                    match_results[active_players[0] + 4] = []

                stat = Scraper.create_stat(active_players,
                                           active_scores,
                                           away_team=True)
                match_results[active_players[0] + 4].append(stat)

                if match_results.get(active_players[1] + 4) is None:
                    match_results[active_players[1] + 4] = []

                stat = Scraper.create_stat(active_players,
                                           active_scores,
                                           reverse=True,
                                           away_team=True)
                match_results[active_players[1] + 4].append(stat)

        return match_results

    @staticmethod
    def create_stat(players, scores, reverse=False, away_team=False):
        """Helper function to create a match results stat.

        **Args:**
            *players*: tuple representing the player game positions.
            For example, ``(1, 2)``

            *scores*: tuple representing the player game results.
            For example, ``(6, 3)``.

            *reverse*: boolean which will create a stat within the
            context of the partner player (second item in the *players*
            tuple)

            *away_team*: boolean which will create a stat within the
            context of the away team (*players* tuple value plus 4)

        **Returns:**
            dictionary structure of the form::

                {
                    'team_mate': 5,
                    'opposition': (1, 2),
                    'score_for': 6,
                    'score_against': 3,
                }

        """
        team_mate = players[1]
        if reverse:
            team_mate = players[0]

        if away_team:
            team_mate += 4

        score_for = scores[0]
        if away_team:
            score_for = scores[1]

        score_against = scores[1]
        if away_team:
            score_against = scores[0]

        inc = 4
        if away_team:
            inc = 0

        stat = {
            'team_mate': team_mate,
            'opposition': (players[0] + inc, players[1] + inc),
            'score_for': score_for,
            'score_against': score_against,
        }

        return stat
