"""Unit test cases for the :class:`trols_stats.DataModel` class.

"""
import unittest
import os
import tempfile

import trols_stats
from filer.files import (get_directory_files_list,
                         remove_files)


class TestDataModel(unittest.TestCase):
    """:class:`trols_stats.DataModel` is the in-memory data model
    construct used by the TROLS Stats platform.

    """
    def test_init(self):
        """Initialise an trols_stats.DataModel object.
        """
        # Given a directory that holds the shelve
        shelve_dir_obj = tempfile.TemporaryDirectory()

        # when I initialise a trols_stats.DataModel
        model = trols_stats.DataModel(shelve=shelve_dir_obj.name)

        # then I should receive an object reference
        msg = 'Object is not a trols_stats.DataModel'
        self.assertIsInstance(model, trols_stats.DataModel, msg)

    def test_construct(self):
        """Construct a TROLS Stats store.
        """
        # Given a source HTML directory location
        source_html_dir = os.path.join('trols_stats',
                                       'tests',
                                       'files',
                                       'cache') 

        # and a shelve directory
        shelve_dir_obj = tempfile.TemporaryDirectory()
        shelve_dir = shelve_dir_obj.name

        # when I construct the datastore
        model = trols_stats.DataModel(shelve=shelve_dir)
        received = model.construct(source_html_dir)

        print('XXX {}'.format(model().keys()))

        # then I should receive a count of tokens stored
        msg = 'Shelve token count error'
        self.assertEqual(received, 40, msg)
