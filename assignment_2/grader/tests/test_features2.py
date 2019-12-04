import unittest

import requests
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, visibility

from utils import *
from config import SERVICE_ADDR


class ExtendedFeatureTest(unittest.TestCase):
    def SetUp(self):
        pass

    @weight(6)
    def test_admin_authorized_history_view(self):
        uname = "authtest1"
        password = "Password@1"
        twofactor = "12345678901"
        user1_s = initSession(uname, password, twofactor)
        sensitive_text = "some sensitive text asdfasdfasdf"
        spellcheck(sensitive_text, uname, password, twofactor, user1_s)
        q_ids = getQueryIds(user1_s, uname)

        self.assertTrue(q_ids is not None, "Could not find query history.")
        self.assertNotEqual(len(q_ids), 0, "Could not find query history.")

        user2_s = requests.Session()
        login("admin", "Administrator@1", "12345678901", user2_s)
        for q_id in q_ids:  # If there are no q_ids?
            qid, uname, text, results = parse_query(
                user2_s.get("%s/history/%s" % (SERVICE_ADDR, q_id))
            )

            if not text:
                qid, uname, text, results = parse_query(
                    user2_s.get("%s/%s/history" % (SERVICE_ADDR, uname))
                )

            self.assertTrue(
                text and sensitive_text in text.text.strip().lstrip(),
                "Admins can't view queries",
            )

    @weight(10)
    def test_unauthorized_history_view(self):
        """
        Check that a users can't view another user's history
        """
        uname = "unauthtest1"
        password = "Password@1"
        twofactor = "12345678901"
        user1_s = initSession(uname, password, twofactor)
        sensitive_text = "some sensitive text asdfasdfasdf"
        spellcheck(sensitive_text, uname, password, twofactor, user1_s)
        q_ids = getQueryIds(user1_s, uname)

        self.assertTrue(q_ids is not None, "Could not find queries.")
        self.assertNotEqual(len(q_ids), 0, "Could not find query history.")

        uname2 = "unauthtest2"
        user2_s = initSession(uname2, password, twofactor)
        for q_id in q_ids:
            qid, uname, text, results = parse_query(
                user2_s.get("%s/history/%s" % (SERVICE_ADDR, q_id))
            )

            if not text:
                qid, uname, text, results = parse_query(
                    s.get("%s/%s/history/%s" % (SERVICE_ADDR, uname, q_id))
                )

            self.assertFalse(
                text and sensitive_text in text, "Users can view unauthorized queries"
            )

    @weight(6)
    def test_history(self):
        uname = "historytest"
        pword = "Password@3"
        twofactor = "12345678901"

        sensitive_text = "some sensitive text asdfasdfasdf"
        s = initSession(uname, pword, twofactor)
        spellcheck(sensitive_text, uname, pword, twofactor, s)

        # Was this even completed?
        q_ids = getQueryIds(s, uname)
        self.assertTrue(q_ids is not None, "Could not find query history.")
        self.assertNotEqual(len(q_ids), 0, "Could not find query history.")

        for q_id in q_ids:  # If there are no q_ids?
            qid, uname, text, results = parse_query(
                s.get("%s/history/%s" % (SERVICE_ADDR, q_id))
            )

            if not text:
                qid, uname, text, results = parse_query(
                    s.get("%s/%s/history/%s" % (SERVICE_ADDR, uame, q_id))
                )

            self.assertTrue(
                text and sensitive_text in text.text, "User can't view queries"
            )
