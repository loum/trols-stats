import trols_stats
from logga.log import log


class Reporter(object):
    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value):
        self.__db = value

    def __init__(self, shelve=None):
        self.__db = trols_stats.DBSession(shelve=shelve)
        self.__db.connect()
