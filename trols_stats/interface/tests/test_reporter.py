import unittest2

import trols_stats.interface as interface


class TestReporter(unittest2.TestCase):
    def test_init(self):
        """Initialise an interface.Reporter object
        """
        reporter = interface.Reporter()
        msg = 'Object is not a interface.Reporter'
        self.assertIsInstance(reporter, interface.Reporter, msg)
