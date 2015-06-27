import unittest2
import os
import mock
import tempfile

import trols_stats.interface as interface
from filer.files import (get_directory_files_list,
                         remove_files,
                         copy_file)


class TestLoader(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__test_dir = os.path.join('trols_stats',
                                      'interface',
                                      'tests',
                                      'files')

    def test_init(self):
        """Initialise a interface.Loader object.
        """
        loader = interface.Loader()
        msg = 'Object is not a interface.Loader'
        self.assertIsInstance(loader, interface.Loader, msg)

    def test_build_game_map(self):
        """build_game_map of a game HTML page.
        """
        # Given a TROLS detailed match results page
        match_popup = 'game_AA039054.html'
        with open(os.path.join(self.__test_dir, match_popup)) as html_fh:
            html = html_fh.read()

        # when a scrape and load occurs
        loader = interface.Loader()
        loader.build_game_map(html)
        received = loader.games

        # then I should receive a list of Game objects
        expected = 16
        msg = 'interface.Loader.games list length should be 8'
        self.assertEqual(len(received), expected, msg)

    def test_request_http(self):
        """Make request to a HTTP resource.
        """
        # Given a match popup URI
        uri = 'http://www.trols.org.au/nejta/match_popup.php'

        # and a payload
        request_args = {'matchid': 'AA026044'}

        # when I make a TROLS request
        html_file = os.path.join(self.__test_dir, 'game_AA026044.html')
        with open(html_file) as _fh:
            html = _fh.read()

        with mock.patch.object(interface.Loader,
                               '_request_url') as mock_request_url:
            mock_request_url.return_value = html
            received = interface.Loader.request(uri, request_args)

            # then I should receive a HTML string response
            expected = html
            msg = 'Expected a HTML response'
            self.assertEqual(expected, received, msg)

    def test_request_http_saved_to_cache(self):
        """Make request to a HTTP resource: saved to cache.
        """
        # Given a match popup URI
        uri = 'http://www.trols.org.au/nejta/match_popup.php'

        # and a payload
        request_args = {'matchid': 'AA026044'}

        # and specify a cache directory
        cache_dir = tempfile.mkdtemp()

        # when I make a TROLS request
        html_file = os.path.join(self.__test_dir, 'game_AA026044.html')
        with open(html_file) as _fh:
            html = _fh.read()

        with mock.patch.object(interface.Loader,
                               '_request_url') as mock_request_url:
            mock_request_url.return_value = html
            interface.Loader.request(uri, request_args, cache_dir)

        # then the HTML response should be saved in the cache
        cache_file = os.path.join(cache_dir, 'game_AA026044.html')
        msg = 'Cached HTML match popup not created'
        self.assertTrue(os.path.exists(cache_file), msg)

        # Clean up.
        remove_files(get_directory_files_list(cache_dir))
        os.removedirs(cache_dir)

    def test_request_http_file_already_cached(self):
        """Make request to a HTTP resource: file already cache.
        """
        # Given a match popup URI
        uri = 'http://www.trols.org.au/nejta/match_popup.php'

        # and a payload
        request_args = {'matchid': 'AA026044'}

        # and specify a cache directory
        cache_dir = tempfile.mkdtemp()

        # and a copy of the request file already cached
        html_file = os.path.join(self.__test_dir, 'game_AA026044.html')
        copy_file(html_file, os.path.join(cache_dir, 'game_AA026044.html'))

        # when I make a TROLS request
        received = interface.Loader.request(uri, request_args, cache_dir)

        # then I should receive a HTML string response
        with open(html_file) as _fh:
            expected = _fh.read()
            msg = 'Expected a HTML response'
            self.assertEqual(expected, received, msg)

        # Clean up.
        remove_files(get_directory_files_list(cache_dir))
        os.removedirs(cache_dir)

    def test_request_http_saved_to_cache_overwrite(self):
        """Make request to a HTTP resource: saved to cache - overwrite.
        """
        # Given a match popup URI
        uri = 'http://www.trols.org.au/nejta/match_popup.php'

        # and a payload
        request_args = {'matchid': 'AA026044'}

        # and specify a cache directory
        cache_dir = tempfile.mkdtemp()

        # and overwrite existing match popup responses
        force_cache = True

        # and an existing match popup exists
        cache_file = os.path.join(cache_dir, 'game_AA026044.html')
        with open(cache_file, 'w'):
            os.utime(cache_file, None)

        # when I make a TROLS request
        with mock.patch.object(interface.Loader,
                               '_request_url') as mock_request_url:
            html_file = os.path.join(self.__test_dir, 'game_AA026044.html')
            with open(html_file) as _fh:
                html = _fh.read()
            mock_request_url.return_value = html
            interface.Loader.request(uri,
                                     request_args,
                                     cache_dir,
                                     force_cache)

        # then the HTML response should be read from the cache
        msg = 'Cached HTML match popup not created'
        self.assertTrue(os.stat(cache_file).st_size > 0, msg)

        # Clean up.
        remove_files(get_directory_files_list(cache_dir))
        os.removedirs(cache_dir)

    def test_request_file(self):
        """Make request to a file resource.
        """
        # Given a file resource on the local file system.
        uri_file = 'trols_stats/tests/files/main_results.php'

        # when I make a TROLS stats request
        received = interface.Loader.request(uri_file)

        # then a value should be received
        msg = 'URI request should not return None'
        self.assertIsNotNone(received, msg)

    @classmethod
    def teatDownClass(cls):
        cls.__test_dir = None
