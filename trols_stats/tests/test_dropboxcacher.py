"""Unit test cases for the :class:`trols_stats.DropBoxCache` class.

"""
import unittest
import pytest
import os

import trols_stats


class TestDropBoxCacher(unittest.TestCase):

    @pytest.mark.skipif(os.environ.get('DROPBOX_TOKEN') is None,
                        reason='Requires a valid Dropbox access token')
    def test_init(self):
        """Initialise a interface.Loader object.
        """
        args = [os.environ.get('DROPBOX_TOKEN')]
        dpcacher = trols_stats.DropBoxCacher(*args)
        msg = 'Object is not a trols_stats.DropBoxCacher'
        self.assertIsInstance(dpcacher, trols_stats.DropBoxCacher, msg)

    @pytest.mark.skipif(os.environ.get('DROPBOX_TOKEN') is None,
                        reason='Requires a valid Dropbox access token')
    def test_list_folder(self):
        """Test listing of TROLS raw HTML files in Dropbox.
        """
        # Given a Dropbox client reference
        args = [os.environ.get('DROPBOX_TOKEN')]
        dpcacher = trols_stats.DropBoxCacher(*args)

        # and a target folder
        path = 'source_raw_html'

        # when I invoke a Dropbox folder listing
        received = dpcacher.list_folder(path) 

        # then I should receive a dictionary of results
        msg = 'Dropbox listing did return matching files'
        self.assertTrue(len(received.keys()), msg)
