"""class:`trols_stats.Scraper`.

Scrape TROLS HTML.

"""
import re
import lxml.html
from logga import log

__all__ = ['Scraper']


class Scraper(object):
    @staticmethod
    def scrape_competition_name(html, xpath, tokenise=False, league=None):
        """Extract the competition name.  For example,
        "Saturday AM - Spring 2015"

        **Args:**
            *html*: string representation of the HTML page to process.

        **Kwargs:**
            *tokenise*: tokenises the competition name to be used as an
            identifier.  For example, ``saturday_am_spring_2015``

            *league*: name of the league from where the matches
            are sourced from

        **Returns:**
            string representation of the compeition name

        """
        root = lxml.html.fromstring(html)
        comp_name = root.xpath(xpath)[0]
        if league is not None:
            comp_name = '{} {}'.format(league.upper(), comp_name)

        log.info('Scraped competition name: %s', comp_name)

        if tokenise:
            comp_name = comp_name.replace(' - ', '_').lower()
            comp_name = comp_name.replace(' ', '_').lower()

        return comp_name

    @staticmethod
    def scrape_competition_ids(html, xpath):
        """Extract the competition IDs.

        **Args:**
            *html*: string representation of the HTML page to process.

        **Returns:**
            dictionary structure representing the competition IDs as the key
            and the competition code as the value.  For example::

                {'GIRLS 1': 'AA026', 'GIRLS 2': 'AA027' ...}

        """
        root = lxml.html.fromstring(html)
        comp_id_elements = root.xpath(xpath)

        comp_ids = {}
        for element in comp_id_elements:
            if (element.attrib.get('value') is not None and
                    element.attrib.get('value') == ''):
                continue

            comp_ids.update(Scraper._get_competition_id(element))

        log.info('Scraped competition IDs: "%s"', comp_ids)

        return comp_ids

    @staticmethod
    def _get_competition_id(element):
        """Competition ID extractor helper.

        **Args:**
            *element*: :class:`lxml.html.HtmlElement` instance generated
            from raw HTML of the form::

                <option value="AA026">GIRLS 1</option>

        **Returns:**
            dictionary structure representing the competition ID as the key
            and the competition code as the value.  For example::

                {'GIRLS 1': 'AA026'}

        """
        comp_id = {element.text: element.attrib['value']}
        log.debug('Competition ID extracted: %s', comp_id)

        return comp_id

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
                    log.warning('Unable to extract match ID from "%s"',
                                attrs)
                    continue

                match_ids.append(match_id)

        log.debug('List of match IDs extracted: "%s"', match_ids)

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
        prog = re.compile(r'open_match\(event,\'.*\',\'(\w+)\'\);')

        match_id = None
        if attributes[0] == 'onclick':
            re_match = prog.match(attributes[1])
            if re_match:
                match_id = re_match.group(1)
                log.debug('Found match ID: %s', match_id)

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
        def get_team_color_code(root, team, xpath, away=False):
            team = team.replace("'", "&apos;")

            color_xpath = xpath % team

            log.debug('Team color xpath "%s"', color_xpath)
            tmp_colors = root.xpath(color_xpath)

            colors = []
            for color in tmp_colors:
                # Some identifiers we don't want.
                clean_color = str.replace(color, '(Late Start)', '')
                if len(clean_color):
                    colors.append(clean_color)

            # Colors could come through for both home and away teams.
            if len(colors):
                if away:
                    team += colors[-1]
                else:
                    team += colors[0]

                log.debug('Color coded team: "%s"', team)

            return team.rstrip()

        root = lxml.html.fromstring(html)
        raw_teams = root.xpath(xpath)

        teams = {}
        if len(raw_teams) != 2:
            log.warning('Expecting two teams. Received %d',
                        len(raw_teams))
        else:
            home_team = raw_teams[0].text
            away_team = raw_teams[1].text

            if color_xpath is not None:
                home_team = get_team_color_code(root,
                                                home_team,
                                                color_xpath)

                away_team = get_team_color_code(root,
                                                away_team,
                                                color_xpath,
                                                away=True)

            teams['home_team'] = home_team.replace(u'\xa0', u' ')
            teams['away_team'] = away_team.replace(u'\xa0', u' ')

        log.debug('Teams extracted: "%s"', teams)

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
        elements = root.xpath(r"//td[re:match(text(), '^\d\.')]/text()",
                              namespaces=namespaces)

        player_re = re.compile(r'^\d\.\s+')
        players = [(i, player_re.sub('', j)) for i, j in enumerate(elements,
                                                                   start=1)]

        log.debug('Players extracted: %s', players)
        return players

    @staticmethod
    def scrape_match_preamble(html, xpath):
        """Extract match preamble from *html*.

        A typical preamble string is as follows::

            GIRLS 1  Rd.1 on 1st Feb 14

        For finals::

            GIRLS 14 Semi Final

        DVTA formats a different::

            Tue Sect 5  Rd.1 on 12th Jul 16

        **Args:**
            *html*: string representation of the HTML page to process.
            *html* is typically a TROLS match results page.

        **Returns:**
            dictionary structure representing components of the
            preamble in the form::

                {
                    'competition_type': <girls|boys|thu>,
                    'section': <section_no>,
                    'date': <date>,
                    'match_round': <round_no>
                }

        """
        root = lxml.html.fromstring(html)
        tmp_preamble = root.xpath(xpath)[0]
        raw_preamble = tmp_preamble.replace(u'\xa0', u' ')

        log.debug('Scraped preamble: "%s"', raw_preamble)

        preamble = {}

        def competition(matchobj):
            preamble['competition_type'] = None

            match_competition = matchobj.group(1).lower()
            if match_competition in ['girls', 'boys']:
                preamble['competition_type'] = match_competition
            log.debug('Match competition_type: "%s"',
                      preamble['competition_type'])

            return matchobj.group(2)

        competition_re = re.compile(r'^(girls|boys|.*?)\s+(.*)',
                                    re.IGNORECASE)
        raw_preamble = competition_re.sub(competition, raw_preamble)

        # Remove the "Sect" and "MWL" token (DVTA only).
        raw_preamble = raw_preamble.replace('Sect ', '')
        raw_preamble = raw_preamble.replace('MWL ', '')

        def section(matchobj):
            match_section = int(matchobj.group(1))
            log.debug('Match section: %d', match_section)
            preamble['section'] = match_section

            return matchobj.group(2)

        section_re = re.compile(r'^(\d+)\s+(.*)')
        raw_preamble = section_re.sub(section, raw_preamble)

        def round_no(matchobj):
            match_round_no = int(matchobj.group(1))
            log.debug('Match round: %d', match_round_no)
            preamble['match_round'] = match_round_no

            return matchobj.group(2)

        round_no_re = re.compile(r'^Rd.(\d+)\s+(.*)')
        raw_preamble = round_no_re.sub(round_no, raw_preamble)

        # Remove the "on" token (both DVTA/NEJTA only).
        raw_preamble = raw_preamble.replace('on ', '')

        def date(matchobj):
            match_date = ('%s %s %s' % (matchobj.group(1),
                                        matchobj.group(3),
                                        matchobj.group(4)))
            log.debug('Match date: %s', match_date)
            preamble['date'] = match_date

            return matchobj.group(5)

        date_re = re.compile(r'^(\d+)(st|nd|rd|th)\s+(\w+)\s+(\d{2})(.*)')
        raw_preamble = date_re.sub(date, raw_preamble)

        def final(matchobj):
            final_token = '{} {}'.format(matchobj.group(1),
                                         matchobj.group(2))
            log.debug('Final token: "%s"', final_token)
            preamble['match_round'] = final_token

            return matchobj.group(3)

        final_re = re.compile(r'^(Semi|Grand) (Final)(.*)')
        raw_preamble = final_re.sub(final, raw_preamble)

        if len(raw_preamble):
            log.warning('Match preamble string has unparsed tokens "%s"',
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
        active_scores = ()
        match_results = {}
        have_home_players = have_scores = False

        # List of raw scores presents as 3 index sets where:
        #   index 1: home player code
        #   index 2: score
        #   index 3: opposition player code
        #
        for score in raw_scores:
            log.debug('Raw score iteration value: %s', score.text)
            count += 1

            if score.text is None:
                log.warning('Parsed invalid raw score component: skipping')
                continue

            if count % 3 == 0:
                log.info('Starting match score parsing segment ...')

                active_players = Scraper.extract_player_codes(score.text)
                log.debug('Home players: %s', active_players)
                have_home_players = True
                continue

            if count % 3 == 1:
                active_scores = [int(x) for x in re.findall(r'\d+',
                                                            score.text)]
                active_scores = tuple(active_scores)
                log.debug('Scores: %s', active_scores)
                if len(active_scores) == 2:
                    have_scores = True
                else:
                    log.warning('Rejecting this score: %s', active_scores)
                continue

            if count % 3 == 2:
                away_players = Scraper.extract_player_codes(score.text)
                log.debug('Away players: %s', away_players)

                active_players = (active_players, away_players)
                log.debug('Active players: %s', active_players)

                if have_home_players and have_scores:
                    match_results.setdefault(active_players[0][0], [])
                    stat = Scraper.create_stat(active_players,
                                               active_scores)
                    match_results[active_players[0][0]].append(stat)

                    if active_players[0][1] is not None:
                        match_results.setdefault(active_players[0][1], [])
                    stat = Scraper.create_stat(active_players,
                                               active_scores,
                                               reverse=True)
                    if active_players[0][1] is not None:
                        match_results[active_players[0][1]].append(stat)

                    match_results.setdefault((active_players[1][0] + 4), [])

                    stat = Scraper.create_stat(active_players,
                                               active_scores,
                                               away_team=True)
                    match_results[(active_players[1][0] + 4)].append(stat)

                    if active_players[1][1] is not None:
                        match_results.setdefault((active_players[1][1] + 4), [])

                    stat = Scraper.create_stat(active_players,
                                               active_scores,
                                               reverse=True,
                                               away_team=True)
                    if active_players[1][1] is not None:
                        match_results[active_players[1][1] + 4].append(stat)
                else:
                    log.warning('Error processing match stats: '
                                'skipping stat creation')

                # Reset state managers.
                active_players = ()
                active_scores = ()
                have_home_players = have_scores = False

                log.info('Match score parsing segment complete.')

        return match_results

    @staticmethod
    def extract_player_codes(raw_player_code):
        """Attempt to extract the player codes from the *raw_player_code*
        HTML segment.

        **Args:**
            *raw_player_code* can present as a singles match format code or
            doubles.  A singles match format code is a single digit.
            Doubles appear present as digits concatentated with a ``+``.
            For example, ``1+2``.

        **Returns:**
            a tuple of tuples representing the player codes.  For example,
            ``1+4`` would return ``((1, 4),)``.  In singles, ``1`` would
           return ``((1, None),)``

        """
        player_codes = [int(x) for x in re.findall(r'\d+', raw_player_code)]
        player_codes += [None] * (2 - len(player_codes))

        return tuple(set(player_codes))

    @staticmethod
    def create_stat(players, scores, reverse=False, away_team=False):
        """Helper function to create a match results stat.

        **Args:**
            *players*: tuples representing the player game positions.
            For example, ``((1, 2), (1, 2))``

            *scores*: tuple representing the player game results.
            For example, ``(6, 3)``.

            *reverse*: boolean which will create a stat within the
            context of the partner player (second item in the *players*
            tuple).  Note: it does not make sense to create a reverse
            stat in singles matches

            *away_team*: boolean which will create a stat within the
            context of the away team (*players* tuple value plus 4)

        **Returns:**
            on success, dictionary structure of the form::

                {
                    'team_mate': 5,
                    'opposition': (1, 2),
                    'score_for': 6,
                    'score_against': 3,
                }

            ``None`` otherwise

        """
        match_is_singles_format = False
        if players[0][1] is None:
            match_is_singles_format = True

        team_mate = players[0][1]
        if not match_is_singles_format and reverse:
            team_mate = players[0][0]

        if not match_is_singles_format and away_team:
            team_mate += 4

        score_for = scores[0]
        if away_team:
            score_for = scores[1]

        score_against = scores[1]
        if away_team:
            score_against = scores[0]

        inc = 4
        away_players_ref = players[1]
        if away_team:
            inc = 0
            away_players_ref = players[0]

        opposition_1 = away_players_ref[0] + inc
        opposition_2 = None
        if away_players_ref[1] is not None:
            opposition_2 = away_players_ref[1] + inc

        stat = None
        if not match_is_singles_format or not reverse:
            stat = {
                'team_mate': team_mate,
                'opposition': (opposition_1, opposition_2),
                'score_for': score_for,
                'score_against': score_against,
            }

        return stat
