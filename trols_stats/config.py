__all__ = ['Config']

import configa
from configa.setter import set_scalar, set_dict


class Config(configa.Config):
    def __init__(self, config_file=None):
        self.__trols_urls = {}
        self.__cache = None
        self.__shelve = None

        configa.Config.__init__(self, config_file)

    @property
    def trols_urls(self):
        return self.__trols_urls

    @set_dict
    def set_trols_urls(self, values=None):
        pass

    @property
    def cache(self):
        return self.__cache

    @set_scalar
    def set_cache(self, value):
        pass

    @property
    def shelve(self):
        return self.__shelve

    @set_scalar
    def set_shelve(self, value):
        pass

    def parse_config(self):
        """Read config items from the configuration file.
        """
        configa.Config.parse_config(self)

        kwargs = [
            {
                'section': 'directories',
                'option': 'cache',
            },
            {
                'section': 'directories',
                'option': 'shelve',
            }
        ]

        for kwarg in kwargs:
            self.parse_scalar_config(**kwarg)

        dict_kwargs = [
            {
                'section': 'trols_urls',
            },
        ]

        for kwarg in dict_kwargs:
            self.parse_dict_config(**kwarg)
