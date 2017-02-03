"""Unit test cases for the :class:`trols_stats.model.entities.Fixture`
class.

"""
import unittest
import json

import trols_stats.model.entities


class TestFixture(unittest.TestCase):
    def test_init(self):
        """Initialise a trols_stats.model.Player object.
        """
        fixture = trols_stats.model.entities.Fixture()
        msg = 'Object is not of type trols_stats.model.Fixture'
        self.assertIsInstance(fixture,
                              trols_stats.model.entities.Fixture,
                              msg)

    def test_to_json(self):
        """Convert trols_stats.model.entities.Fixture() object to JSON.
        """
        # Given a fixture data structure
        fixture_data = {
            'uid': 1234,
            'competition': 'saturday_am_autumn_2015',
            'competition_type': 'girls',
            'section': 14,
            'date': '28 Feb 15',
            'match_round': 5,
            'home_team': 'Watsonia Red',
            'away_team': 'St Marys',
        }

        # when I create a trols_stats.model.entities.Fixture object
        fixture = trols_stats.model.entities.Fixture(**fixture_data)

        # and dump to JSON
        received = json.loads(fixture.to_json())

        # then I should get a serialised JSON string
        expected = {
            "date": "28 Feb 15",
            "home_team": "Watsonia Red",
            "away_team": "St Marys",
            "uid": 1234,
            "competition_type": "girls",
            "section": 14,
            "competition": "saturday_am_autumn_2015",
            "match_round": 5
        }
        msg = 'trols_stats.model.entities.Fixture() to JSON error'
        self.assertDictEqual(received, expected, msg)
