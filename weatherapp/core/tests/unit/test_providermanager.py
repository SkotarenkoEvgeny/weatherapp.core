import unittest

from weatherapp.core.providermanager import ProviderManager


class DummyProvider:
    pass


class ProviderManagerTestCase(unittest.TestCase):
    """
        Unit test case for provider manager.
        """

    def setUp(self):
        self.provider_manager = ProviderManager()

    def test_add(self):
        """
        Test add method for provider manager.
        """
        self.provider_manager.add('dummy', DummyProvider)
        self.assertTrue('dummy' in self.provider_manager._providers)
        self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)

    def test_get(self):
        """
        Test application get method.
        """
        self.provider_manager.add('dummy', DummyProvider)
        self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)

    def test_contain(self):
        """
        Test if '__contains__' method is working.
        """
        self.provider_manager.add('dummy', DummyProvider)
        self.assertTrue('dummy' in self.provider_manager._providers)
        self.assertFalse('bar' in self.provider_manager._providers)


if __name__ == '__main__':
    unittest.main()
