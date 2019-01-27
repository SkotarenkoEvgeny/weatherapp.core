from weatherapp.core.abstract import Command
from weatherapp.core import config

class Providers(Command):

    """
    Print all available providers.
    """

    sites = config.sites

    @staticmethod
    def providers():
        return Providers.sites

    def run(self):
        for name in Providers.sites:
            print(name)
