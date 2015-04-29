import trols_stats.model

__all__ = ['Fixture']


class Fixture(trols_stats.model.Base):
    """
    .. attribute:: match_round
    .. attribute:: competition
    .. attribute:: section
    .. attribute:: date
    .. attribute:: home_team
    .. attribute:: away_team

    """
    @property
    def match_round(self):
        return self.__round

    @match_round.setter
    def match_round(self, value):
        self.__round = value

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
                 uid=None,
                 match_round=None,
                 competition=None,
                 section=None,
                 date=None,
                 home_team=None,
                 away_team=None):
        super(Fixture, self).__init__(uid=uid)

        self.__round = match_round
        self.__competition = competition
        self.__section = section
        self.__date = date
        self.__home_team = home_team
        self.__away_team = away_team

    def __call__(self):
        return {
            'uid': self.uid,
            'match_round': self.match_round,
            'competition': self.competition,
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
                'section': self.section,
                'date': self.date,
                'match_round': self.match_round,
                'home_team': self.home_team,
                'away_team': self.away_team,
            }
            is_same = (cmp(fixture, other) == 0)
        else:
            is_same = self.__dict__ == other.__dict__

        return is_same
