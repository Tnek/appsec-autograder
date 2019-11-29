import unittest

from gradescope_utils.autograder_utils.decorators import weight, visibility

from utils import *


class SqlFixture(unittest.TestCase):
    def SetUp(self):
        pass

    @weight(10)
    def test_sqli(self):
        payload = "' or 1=1 -- "

        self.assertFalse(
            login(payload, payload, payload), "There is sql injection in your code"
        )
