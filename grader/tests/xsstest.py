import unittest
from text_fixture import WebFixture
from gradescope_utils.autograder_utils.decorators import weight, visibility


class TestXSS(WebFixture):
    @weight(1)
    def xss_runner(self):
        pass
