import abc
import json

"""Base class for all objects in the TROLS Stats data model.

"""
__all__ = ['Base']


class Base(object):
    """This is a abstract class that must be inherited.

    """
    __metaclass__ = abc.ABCMeta

    def to_json(self):
        return json.dumps(self())
