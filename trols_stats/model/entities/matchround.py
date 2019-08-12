""":class:`trols_stats.model.entities.MatchRound`

"""
import re

import trols_stats.model

__all__ = ['MatchRound']


class MatchRound(trols_stats.model.Base):
    """Abstraction of a match round number.

    Enables support for numeric round numbers in addition to
    string representations such as "Semi Final", "Prelim Final" and "Grand Final".

    """
    def __init__(self, match_round=None):
        """Take string representation of match round and create a numeric
        equivalent.

        """
        self.__match_round = match_round
        self.__match_round_numeric = match_round

        if match_round is not None and isinstance(match_round, str):
            if re.match('[0-9]+', match_round):
                self.__match_round_numeric = int(match_round)
            elif match_round.lower() == 'semi final':
                self.__match_round_numeric = 100
            elif match_round.lower() == 'prelim final':
                self.__match_round_numeric = 1000
            elif match_round.lower() == 'grand final':
                self.__match_round_numeric = 10000

    def __call__(self, as_number=False):
        value = self.__match_round
        if as_number:
            value = self.__match_round_numeric

        return value
