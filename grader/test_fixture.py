import unittest

import requests
from gradescope_utils.autograder_utils.decorators import weight, visibility

from config import SERVICE_ADDR, REPORTER_ADDR


class WebFixture(unittest.TestCase):
    def SetUp(self):
        self.SERVICE_ADDR = SERVICE_ADDR
        self.REPORTER_ADDR = REPORTER_ADDR


