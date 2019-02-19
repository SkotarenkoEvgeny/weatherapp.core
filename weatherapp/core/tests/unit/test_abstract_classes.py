import unittest
from unittest.mock import patch

from weatherapp.core.abstract import Command
from weatherapp.core.abstract import Formatter
from weatherapp.core.abstract import Manager


class AbstractTestCase(unittest.TestCase):
    """
    Unit test case for abstract classes.
    """

    @patch.multiple(Command, __abstractmethods__=set())
    def test_command(self):
        """
        test for abstract class Command
        """
        self.instance = Command('site_name', 'app')
        self.assertIsInstance(self.instance, Command)

    @patch.multiple(Formatter, __abstractmethods__=set())
    def test_formatter(self):
        """
        test for abstract class Formatter
        """
        self.instance = Formatter()
        self.assertIsInstance(self.instance, Formatter)

    @patch.multiple(Manager, __abstractmethods__=set())
    def test_manager(self):
        """
        test for abstract class Formatter
        """
        self.instance = Manager()
        self.assertIsInstance(self.instance, Manager)


if __name__ == '__main__':
    unittest.main()
