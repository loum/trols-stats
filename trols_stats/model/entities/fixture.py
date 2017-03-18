""":class:`trols_stats.model.entities.Fixture`

"""
import trols_stats.model
import time
import datetime

__all__ = ['Fixture']


class Fixture(trols_stats.model.Base):
    """
    .. attribute:: match_round
        :class:`trols_stats.model.entities.MatchRound` object instance

    .. attribute:: competition_type

    .. attribute:: competition

    .. attribute:: section

    .. attribute:: date

    .. attribute:: home_team

    .. attribute:: away_team

    """
    @property
    def match_round(self):
        return self.__round()

    @property
    def match_round_numeric(self):
        return self.__round(as_number=True)

    @match_round.setter
    def match_round(self, value):
        self.__round = None
        del self.__round
        self.__round = trols_stats.model.entities.MatchRound(value)

    @property
    def competition_type(self):
        return self.__competition_type

    @competition_type.setter
    def competition_type(self, value):
        self.__competition_type = value

    @property
    def competition(self):
        return self.__competition

    @competition.setter
    def competition(self, value):
        self.__competition = value

    @property
    def section(self):
        return self.__section

    @section.setter
    def section(self, value):
        self.__section = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def home_team(self):
        return self.__home_team

    @home_team.setter
    def home_team(self, value):
        self.__home_team = value

    @property
    def away_team(self):
        return self.__away_team

    @away_team.setter
    def away_team(self, value):
        self.__away_team = value

    def __init__(self,
                 match_round=None,
                 competition_type=None,
                 competition=None,
                 section=None,
                 date=None,
                 home_team=None,
                 away_team=None):

        self.__round = trols_stats.model.entities.MatchRound(match_round)
        self.__competition_type = competition_type
        self.__competition = competition
        self.__section = section
        self.__date = date
        self.__home_team = home_team
        self.__away_team = away_team

    def __call__(self):
        return {
            'match_round': self.match_round,
            'competition': self.competition,
            'competition_type': self.competition_type,
            'section': self.section,
            'date': self.date,
            'home_team': self.home_team,
            'away_team': self.away_team,
        }

    def __eq__(self, other):
        is_same = False

        if isinstance(other, dict):
            fixture = {
                'competition': self.competition,
                'competition_type': self.competition_type,
                'section': self.section,
                'date': self.date,
                'match_round': self.match_round,
                'home_team': self.home_team,
                'away_team': self.away_team,
            }
            is_same = fixture == other
        else:
            is_same = self.__dict__ == other.__dict__

        return is_same

    def comvert_match_date(self):
        """Convert a NEJTA date format to a more human readable form.

        **Args:**
            *date*: NEJTA date in the form DD MM YY.  For example,
            "30 Nov 00"

        **Returns**:
            :mod:`datetime.datetime` object representation

        """
        dt = None
        if self.date is not None:
            time_struct = time.strptime(self.date, "%d %b %y")
            dt = datetime.datetime.fromtimestamp(time.mktime(time_struct))

        return dt
