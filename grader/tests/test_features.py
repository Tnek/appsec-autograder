import unittest

import requests
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, visibility

from utils import *


class FeatureTest(unittest.TestCase):
    def SetUp(self):
        pass

    @weight(1)
    def test_page_exists(self):
        """
        Check that all the required pages for a working application exist
        """
        PAGES = ["/register", "/login", "/spell_check"]
        for page in PAGES:
            r = requests.get(SERVICE_ADDR + page)
            self.assertEqual(r.status_code, 200)

    @weight(1)
    def test_invalid_auth(self):
        """
        Checks that invalid creds fail
        """
        login_addr = SERVICE_ADDR + "/login"

        r = requests.post(
            reg_addr, data={"uname": "null", "pword": "null", "2fa": "1234"}
        )

        result = getElementById(r.text, "result")
        self.assertTrue("incorrect" in result.text)

    @weight(1)
    def test_xsrf(self):
        uname = "xsrf_test"
        pword = "password"
        twofactor = "1234567890"
        s = initSession(uname, pword, twofactor)

        form = getSpellcheckForm(s)
        inputs = input_form.find_all("input")

        token, remainder = filterXsrfToken(inputs)
        self.assertIsNotNone(token)

    @weight(1)
    def test_spellcheck(self):
        spellcheck("test", "spellcheck_test", "pword", "1234567890")
