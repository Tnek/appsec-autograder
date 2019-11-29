import asyncio
import time
import unittest
import requests

from gradescope_utils.autograder_utils.decorators import weight, visibility

from utils import *
from xssbot import *
from config import SERVICE_ADDR


class AdminXssFixture(unittest.TestCase):
    def SetUp(self):
        pass

    @weight(5)
    def test_admin_xss(self):
        admin_s = requests.Session()
        uname = "admin"
        pword = "Administrator@1"
        twofactor = "12345678901"
        ok = login(uname, pword, twofactor, admin_s)
        assert ok, "Admin login failed with uname=%s, pword=%s, and 2fa=%s" % (
            uname,
            pword,
            twofactor,
        )

        uname = "testadminxss"
        pword = "testadminxss"
        twofactor = "31333333337"
        s = initSession(uname, pword, twofactor)

        spellcheck_exploit = lambda payload: spellcheck(
            payload, uname, password, twofactor, s
        )

        # payload = build_payload()
        # spellcheck(payload, uname, password, twofactor, s)
        queries = getQueryIds(s, uname)
        self.assertNotEqual(len(queries), 0, "Cannot get query history.")

        time.sleep(1)

        sid = "admin_history_xss"

        asyncio.ensure_future(
            inquisition(spellcheck_exploit, "%s/spellcheck" % (SERVICE_ADDR), sid, s)
        )

        for queryid in queries:
            asyncio.ensure_future(
                inquisition(
                    lambda: True,
                    "%s/%s/history/%s" % (SERVICE_ADDR, uname, queryid),
                    sid,
                    admin_s,
                )
            )
        time.sleep(1)

        report = fetch_report(sid)

        # Check if callback report is empty
        self.assertFalse(bool(report), "There is XSS on the admin panel of your code")

    @weight(5)
    def test_spellcheck_history_xss(self):
        uname = "history_xss_test"
        pword = "password"
        twofactor = "1234567890"
        s = initSession(uname, pword, twofactor)

        spellcheck_exploit = lambda payload: spellcheck(
            payload, uname, password, twofactor, s
        )

        sid = "history_xss_test"
        asyncio.ensure_future(
            inquisition(spellcheck_exploit, "%s/spellcheck" % (SERVICE_ADDR), sid, s)
        )

        asyncio.ensure_future(
            inquisition(lambda: True, "%s/%s/history" % (SERVICE_ADDR, uname), sid, s)
        )
        time.sleep(1)

        queries = getQueryIds(s, uname)
        self.assertNotEqual(len(queries), 0, "Cannot get query history.")

        for queryid in queries:
            asyncio.ensure_future(
                inquisition(
                    lambda: True,  # Sorry, ugly hack for no-op prior to an inquisition
                    "%s/%s/history/%s" % (SERVICE_ADDR, uname, queryid),
                    sid,
                    s,
                )
            )

        time.sleep(len(queries))

        report = fetch_report(sid)

        # Check if callback report is empty
        self.assertFalse(
            bool(report), "There is XSS in the history section of your code"
        )
