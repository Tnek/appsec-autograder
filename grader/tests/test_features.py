import unittest

import requests
from gradescope_utils.autograder_utils.decorators import weight, visibility

from utils import *
from config import SERVICE_ADDR


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

        login("null", "null", "1234")
        self.assertFalse(login, "Login authenticated an invalid uname/password/2fa")

    @weight(1)
    def test_xsrf(self):
        uname = "xsrf_test"
        pword = "password"
        twofactor = "1234567890"
        s = initSession(uname, pword, twofactor)

        form = getSpellcheckForm(s)
        inputs = form.find_all("input")

        token, remainder = filterXsrfToken(inputs)
        self.assertIsNotNone(token, "Missing csrf token")

        # Check for repeating xsrf token
        s = initSession(uname + "2", pword, twofactor)
        form = getSpellcheckForm(s)
        inputs = form.find_all("input")

        second_token, remainder = filterXsrfToken(inputs)
        self.assertNotEqual(
            second_token.get("value"), token.get("value"), "Using static CSRF token"
        )

    @weight(1)
    def test_spellcheck(self):
        spellcheck("test", "spellcheck_test", "pword", "1234567890")
