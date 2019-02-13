from weatherapp.core.abstract import Command
from weatherapp.core import config

class Providers(Command):

    """
    Print all available providers.
    """

    sites = config.sites
    name = "providers"

    @staticmethod
    def providers():
        return Providers.sites

    def run(self, argv):
        for name in Providers.sites:
            print(name)
