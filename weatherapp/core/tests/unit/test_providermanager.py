import unittest

from weatherapp.core.providermanager import ProviderManager


class DummyProvider:
    pass

class ProviderManagerTestCase(unittest.TestCase):


    def setUp(self):
        self.provider_manager = ProviderManager()


    def test_add(self):
        """
        Test add method for command manager.
        """
        print(self.provider_manager)
        # print(self.provider_manager._providers)

    #     self.provider_manager.add('dummy', DummyProvider)
    #     self.assertTrue('dummy' in self.provider_manager._providers)
    #     self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)


if __name__ == '__main__':
    unittest.main()
