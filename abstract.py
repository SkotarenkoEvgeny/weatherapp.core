'''
Abstract clases for project
'''
import abc
import argparse
import sys, os
import requests
import time
import hashlib

from configparser import ConfigParser
from bs4 import BeautifulSoup

import config


class Command(abc.ABC):
    '''Base class for commands'''

    def __init__(self, site_name):
        self.site_name = site_name

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self, argv):
        '''
        Invoced by application when the command is run
        '''