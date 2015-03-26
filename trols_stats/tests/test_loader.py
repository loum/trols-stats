import unittest2

import trols_stats


class TestLoader(unittest2.TestCase):

    def test_init(self):
        """Initialise a trols_stats.Loader object.
        """
        loader = trols_stats.Loader()
        msg = 'Object is not a trols_stats.Loader'
        self.assertIsInstance(loader, trols_stats.Loader, msg)
