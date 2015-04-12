import unittest2

import trols_stats.interface


class TestLoader(unittest2.TestCase):

    def test_init(self):
        """Initialise a trols_stats.interface.Loader object.
        """
        loader = trols_stats.interface.Loader()
        msg = 'Object is not a trols_stats.interface.Loader'
        self.assertIsInstance(loader, trols_stats.interface.Loader, msg)
