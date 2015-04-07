import abc
import json

__all__ = ['Base']


class Base(object):
    """
    .. attribute:: uid

    """
    __metaclass__ = abc.ABCMeta

    @property
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, value):
        self.__uid = value

    def __init__(self, uid=None):
        self.__uid = uid

    def to_json(self):
        return json.dumps(self())
