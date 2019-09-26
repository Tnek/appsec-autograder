import unittest

import requests
from gradescope_utils.autograder_utils.decorators import weight, visibility

SERVICE_ADDR = "http://127.0.0.1:5000"
REPORTER_ADDR = "http://127.0.0.1:31337"


class WebFixture(unittest.TestCase):
    def SetUp(self):
        self.SERVICE_ADDR = SERVICE_ADDR
        self.REPORTER_ADDR = REPORTER_ADDR
