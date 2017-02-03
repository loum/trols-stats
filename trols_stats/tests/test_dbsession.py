"""Unit test cases for the :class:`trols_stats.DBSession` class.

"""
import unittest
import os
import tempfile

import trols_stats
from filer.files import (get_directory_files_list,
                         remove_files)


class TestDBSession(unittest.TestCase):
    def test_init(self):
        """Initialise an trols_stats.DBSession object
        """
        dbsession = trols_stats.DBSession()
        msg = 'Object is not a trols_stats.DBSession'
        self.assertIsInstance(dbsession, trols_stats.DBSession, msg)

    def test_connect(self):
        """Connect to DB.
        """
        # Given a shelve DB connection.
        shelve_dir = tempfile.mkdtemp()

        # when I attempt to connect to the DB.
        kwargs = {
            'shelve': shelve_dir,
        }
        dbsession = trols_stats.DBSession(**kwargs)
        received = dbsession.connect()

        # then I should receive success status.
        msg = 'Shelve DB connection should return True'
        self.assertTrue(received, msg)

        # Clean up.
        del dbsession
        remove_files(get_directory_files_list(shelve_dir))
        os.removedirs(shelve_dir)
