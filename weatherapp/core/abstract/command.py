import abc
import argparse


class Command(abc.ABC):
    """
    Base class for commands
    """

    call = 0

    def __init__(self, site_name):
        self.site_name = site_name

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self):
        """
        Invoiced by application when the command is run
        """
