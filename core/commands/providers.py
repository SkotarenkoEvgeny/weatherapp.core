from weatherapp.core.abstract import Command


class Prowiders(Command):

    """
    Print all available providers.
    """

    sites = config.sites

    @staticmethod
    def providers():
        return sites

    def run():
        for name in sites:
            print(name)
