"""Unit test cases for the :class:`trols_stats.model.entities.Player`
class.

"""
import unittest


import trols_stats.model.entities


class TestMatchRound(unittest.TestCase):

    def test_init(self):
        """Initialise a trols_stats.model.entities.MatchRound object.
        """
        player = trols_stats.model.entities.MatchRound()
        msg = 'Object is not of type trols_stats.model.entities.MatchRound'
        self.assertIsInstance(player,
                              trols_stats.model.entities.MatchRound,
                              msg)

    def test_init_match_round(self):
        """Initialise a trols_stats.model.entities.MatchRound.
        """
        # Given a "Semi Final" match
        match_round = trols_stats.model.entities.MatchRound('1')

        # when I call the object as a string
        received = match_round()

        # then I should match the token "1"
        msg = 'String representation of Match Round error'
        self.assertEqual(received, '1', msg)

        # and when I call the object as a number
        received = match_round(as_number=True)

        # and the numeric representation should be 1
        msg = 'Numeric representation of Match Round error'
        self.assertEqual(received, 1, msg)

    def test_init_semi_final(self):
        """Initialise a trols_stats.model.entities.MatchRound: Semi Final.
        """
        # Given a "Semi Final" match
        match_round = trols_stats.model.entities.MatchRound('Semi Final')

        # when I call the object as a string
        received = match_round()

        # then I should match the token "Semi Final"
        expected = 'Semi Final'
        msg = 'String representation of Match Round (Semi Final) error'
        self.assertEqual(received, expected, msg)

        # and when I call the object as a number
        received = match_round(as_number=True)

        # and the numeric representation should be 100
        msg = 'Numeric representation of Match Round (Semi Final) error'
        self.assertEqual(received, 100, msg)

    def test_init_prelim_final(self):
        """Initialise a trols_stats.model.entities.MatchRound: Prelim Final.
        """
        # Given a "Prelim Final" match
        match_round = trols_stats.model.entities.MatchRound('Prelim Final')

        # when I call the object as a string
        received = match_round()

        # then I should match the token "Prelim Final"
        expected = 'Prelim Final'
        msg = 'String representation of Match Round (Prelim Final) error'
        self.assertEqual(received, expected, msg)

        # and when I call the object as a number
        received = match_round(as_number=True)

        # and the numeric representation should be 1000
        msg = 'Numeric representation of Match Round (Prelim Final) error'
        self.assertEqual(received, 1000, msg)

    def test_init_grand_final(self):
        """Initialise a trols_stats.model.entities.MatchRound: Grand Final.
        """
        # Given a "Grand Final" match
        match_round = trols_stats.model.entities.MatchRound('Grand Final')

        # when I call the object as a string
        received = match_round()

        # then I should match the token "Grand Final"
        expected = 'Grand Final'
        msg = 'String representation of Match Round (Grand Final) error'
        self.assertEqual(received, expected, msg)

        # and when I call the object as a number
        received = match_round(as_number=True)

        # and the numeric representation should be 10000
        msg = 'Numeric representation of Match Round (Grand Final) error'
        self.assertEqual(received, 10000, msg)
