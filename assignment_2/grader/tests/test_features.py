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
            #self.assertEqual(r.status_code, 200)
            if page != "/spell_checl":
                self.assertEqual(r.status_code, 200)
            else:
                self.assertTrue(r.status_code == 401 or r.status_code == 403 or r.status_code == 200)

    @weight(3)
    def test_invalid_auth(self):
        """
        Checks that invalid creds fail
        """
        login_addr = SERVICE_ADDR + "/login"

        ok = login("null", "null", "1234")
        self.assertFalse(ok, "Login authenticated an invalid uname/password/2fa")

    @weight(2)
    def test_xsrf(self):
        uname = "xsrf_test"
        pword = "password"
        twofactor = "17572028961"
        uname2 = "xsrf_test2"
        pword2 = "password2"
        twofactor2 = "17572028962"
        s = initSession(uname, pword, twofactor)

        form, soup = getSpellcheckForm(s)
        inputs = soup.find_all("input")

        token, remainder = filterXsrfToken(inputs)
        self.assertIsNotNone(token, "Missing csrf token")

        # Check for repeating xsrf token
        s2 = initSession(uname2, pword2, twofactor2)
        new_form, new_soup = getSpellcheckForm(s2)
        new_inputs = new_soup.find_all("input")
        second_token, new_remainder = filterXsrfToken(new_inputs)
        self.assertIsNotNone(second_token, "Missing CSRF token")

        self.assertNotEqual(
            second_token.get("value"), token.get("value"), "Using static CSRF token"
        )  

    @weight(2)
    def test_spellcheck(self):
        sensitive_text = "some sensitive text asdfasdfasdf"
        spellcheck(sensitive_text, "spellchecktest", "Password1!", "17572028962")
