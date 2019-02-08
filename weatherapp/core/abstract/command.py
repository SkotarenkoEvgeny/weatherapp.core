import abc
import argparse


class Command(abc.ABC):
    """
    Base class for commands
    :param app: Main application instance
    :type app: `app.App`
    """

    call = 0

    def __init__(self, site_name, app):
        self.site_name = site_name
        self.app = app

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self, argv):
        """
        Invoiced by application when the command is run
        """
