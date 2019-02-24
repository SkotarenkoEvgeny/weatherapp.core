import unittest

from weatherapp.core.app import App

from argparse import ArgumentParser
import sys
import logging

from weatherapp.core import config

from weatherapp.core.providermanager import ProviderManager
from weatherapp.core.commandmanager import CommandManager
from weatherapp.core.formatters import TableFormatter, CSV_Formatter


class AppTestCase(unittest.TestCase):
    """
    test for App
    """

    def setUp(self):
        self.test_app = App()

    def test_App_instance(self):
        """
        Test App
        """
        self.assertIsInstance(self.test_app, App)

    def test_argparse(self):
        """
        Test application argparse.
        """
        test_parsed_args = self.test_app.arg_parser.parse_args(["accu"])
        self.assertEqual(test_parsed_args.command, 'accu')
        self.assertIsNot(test_parsed_args, 'temp')
        self.assertFalse(test_parsed_args.debug, True)

    def test_loads_formatter(self):
        """
        Test application _load_formatter.
        """

        formatter = {'table': TableFormatter, 'csv': CSV_Formatter}
        self.assertDictEqual(formatter, self.test_app._load_formatter())


if __name__ == '__main__':
    unittest.main()
