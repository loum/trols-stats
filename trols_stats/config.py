__all__ = ['Config']

import configa
from configa.setter import set_scalar


class Config(configa.Config):
    def __init__(self, config_file=None):
        self.__main_results = None

        configa.Config.__init__(self, config_file)

    @property
    def main_results(self):
        return self.__main_results

    @set_scalar
    def set_main_results(self, value):
        pass
 

    def parse_config(self):
        """Read config items from the configuration file.
        """
        configa.Config.parse_config(self)

        kwargs = [
            {
                'section': 'trols_urls',
                'option': 'main_results',
            }
        ]

        for kwarg in kwargs:
            self.parse_scalar_config(**kwarg)
