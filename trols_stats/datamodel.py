""":class:`trols_stats.DataModel`

"""
import os
import logging

import trols_stats.interface
from filer.files import get_directory_files


class DataModel(object):
    """TROLS Stats data model.

    """
    content = {}

    def __init__(self, shelve):
        self.__session = trols_stats.DBSession(shelve=shelve)
        self.__session.connect()
        self.__content = self.__session.connection.get('trols')

    def __call__(self):
        return self.__content

    def construct(self, raw_data_directory=os.curdir):
        """Source raw HTML files from *raw_data_directory* and
        build the data store.

        **Kargs:**
            *raw_data_directory*: location of source HTML files.  Defaults
            to the current directory if not provided

        """
        loader = trols_stats.interface.Loader()

        for html_file in get_directory_files(raw_data_directory,
                                             file_filter=r'.*.html$'):
            with open(html_file) as _fh:
                loader.build_game_map(_fh.read(),
                                      os.path.basename(html_file))

        player_id_games = {}
        for game in loader.games:
            token = game.player_id().get('token')
            player_id_games.setdefault(token, [])
            player_id_games[token].append(game)

        token_count = len(player_id_games.keys())

        self.__session.connection['trols'] = player_id_games
        self.__content = player_id_games
        logging.info('%d games written to "%s"',
                     token_count, self.__session.shelve_db)

        return token_count
