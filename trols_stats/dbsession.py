"""class:`trols_stats.DBSession`.

"""
import os
import shelve

import logging
from filer.files import create_dir


class DBSession(object):
    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, value):
        self.__connection = value

    @property
    def shelve_db(self):
        return self.__shelve_db

    @shelve_db.setter
    def shelve_db(self, value):
        self.__shelve_db = value

    def __init__(self, **kwargs):
        self.__connection = None
        self.__shelve_db = kwargs.get('shelve')

    def __del__(self):
        if self.connection and self.shelve_db:
            self.connection.close()

    def connect(self):
        """Create a database session connection based on class attributes.

        """
        status = False

        if self.shelve_db is not None:
            logging.info('DB session (shelve): starting ...')
            if create_dir(self.shelve_db):
                shelve_path = os.path.join(self.shelve_db,
                                           'trols_stats.db')
                logging.debug('Shelve DB path "%s"', shelve_path)
                flag = 'r'
                if not os.path.exists(shelve_path):
                    logging.info('Creating data store')
                    flag = 'c'
                logging.debug('DB open flag: "%s"', flag)
                self.connection = shelve.open(shelve_path, flag=flag)
                status = True

        logging.info('DB (shelve) connection status: %s', status)

        return status
