import unittest2

import trols_stats


class TestStore(unittest2.TestCase):
    def test_init(self):
        """Initialise a trols_stats.interface.Loader object.
        """
        store = trols_stats.Store()
        msg = 'Object is not a trols_stats.Store'
        self.assertIsInstance(store, trols_stats.Store, msg)
