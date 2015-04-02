import unittest2

import trols_stats


class TestFixture(unittest2.TestCase):
    def test_init(self):
        """Initialise a trols_stats.Player object.
        """
        fixture = trols_stats.Fixture()
        msg = 'Object is not of type trols_stats.Fixture'
        self.assertIsInstance(fixture, trols_stats.Fixture, msg)
