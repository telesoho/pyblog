import unittest

from lib.yundama import YDMHttp

class TestYDMHttpMethods(unittest.TestCase):
    """
    Test YDMHttp class
    """
    ydmhttp = None

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.ydmhttp = YDMHttp('tanbunko', 'tanwen', 3507, 'fbc022f075783db777c02261e8e9d440')

    def test_login(self):
        """
        Login test
        """
        ret = self.ydmhttp.login()
        self.assertNotEqual(ret, -9001)
        self.assertTrue(ret == 47954)


    def test_split(self):
        """
        Balance test
        """
        bal = self.ydmhttp.balance()
        self.assertNotEqual(bal, -9001)
        self.assertTrue(bal > 0)

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

if __name__ == '__main__':
    unittest.main()

