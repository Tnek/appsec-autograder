import re
import requests

from bs4 import BeautifulSoup
from config import SERVICE_ADDR


def parse_query(res):
    res_text = res.text
    soup = BeautifulSoup(res_text, "html.parser")
    qid = soup.find(id="queryid")
    uname = soup.find(id="username")
    text = soup.find(id="querytext")
    results = soup.find(id="queryresults")
    return qid, uname, text, results


def getElementById(text, eid):
    soup = BeautifulSoup(text, "html.parser")
    result = soup.find(id=eid)
    return result


def getFormMethod(text, eid):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find("form", id=eid).get("method")


def filterXsrfToken(soup_list):
    remainder = []
    xsrf_token = None

    for soup in soup_list:
        input_elem = soup.get("name")
        if not input_elem:
            continue

        input_name = input_elem.lower()

        if "xsrf" in input_name or "csrf" in input_name:
            xsrf_token = soup
        else:
            remainder.append(soup)

    return xsrf_token, remainder


def getSpellcheckForm(sess=None):
    if sess == None:
        sess = requests.Session()
    spellcheck_addr = SERVICE_ADDR + "/spell_check"
    r = sess.get(spellcheck_addr)

    soup = BeautifulSoup(r.text, "html.parser")
    input_form = soup.find("input", id="inputtext")
    if not input_form:
        input_form = soup.find("textarea", id="inputtext")
    return input_form, soup


def registerAccount(uname, pword, twofactor, session=None):
    addr = SERVICE_ADDR + "/register"
    if session is None:
        session = requests.Session()

    addr = SERVICE_ADDR + "/register"
    r = session.get(addr)
    soup = BeautifulSoup(r.text, "html.parser")
    # TODO: FIX ME, CONTINUE FROM HERE
    # form = soup.find("form", id="TODO: FILL IN ID")
    form = soup.find_all("form")
    assert len(form) == 1, "More than one form on the page?"
    form = form[0]

    inputs = form.find_all("input")
    token, remainder = filterXsrfToken(inputs)

    uname_form = soup.find("input", id="uname")
    pword_form = soup.find("input", id="pword")
    twofactor_form = soup.find("input", id="2fa")

    assert uname_form is not None, "Could not find uname input."
    assert pword_form is not None, "Could not find pword input."
    assert twofactor_form is not None, "Could not find 2fa input."

    if token is not None:
        test_creds = {
            uname_form.get("name"): uname,
            pword_form.get("name"): pword,
            twofactor_form.get("name"): twofactor,
            token.get("name"): token.get("value"),
        }
    else:
        test_creds = {
            uname_form.get("name"): uname,
            pword_form.get("name"): pword,
            twofactor_form.get("name"): twofactor,
        }

    r = session.post(addr, data=test_creds)
    success = getElementById(r.text, "success")
    assert success != None, "Missing id='success' in your register response"
    return "success" in success.text.lower()


def login(uname, pword, twofactor, session=None):
    addr = SERVICE_ADDR + "/login"
    if session is None:
        session = requests.Session()

    r = session.get(addr)
    soup = BeautifulSoup(r.text, "html.parser")
    # TODO: FIX ME, CONTINUE FROM HERE
    # form = soup.find("form", id="TODO: FILL IN ID")
    form = soup.find_all("form")
    assert len(form) == 1
    form = form[0]

    inputs = form.find_all("input")
    token, remainder = filterXsrfToken(inputs)

    # TODO: FIX ME, USE NAME ATTRIBUTES GRABBED BY INPUT IDs.
    uname_form = soup.find("input", id="uname")
    pword_form = soup.find("input", id="pword")
    twofactor_form = soup.find("input", id="2fa")

    assert uname_form is not None, "Could not find uname input."
    assert pword_form is not None, "Could not find pword input."
    assert twofactor_form is not None, "Could not find 2fa input."

    if token is not None:
        test_creds = {
            uname_form.get("name"): uname,
            pword_form.get("name"): pword,
            twofactor_form.get("name"): twofactor,
            token.get("name"): token.get("value"),
        }
    else:
        test_creds = {
            uname_form.get("name"): uname,
            pword_form.get("name"): pword,
            twofactor_form.get("name"): twofactor,
        }

    r = session.post(addr, data=test_creds)
    success = getElementById(r.text, "result")
    assert success != None, "Missing id='result' in your login response"
    return "success" in success.text.lower()


def initSession(uname, pword, twofactor):
    s = requests.Session()
    ok = registerAccount(uname, pword, twofactor, s)
    assert ok, "Registration failed with uname=%s, pword=%s, and 2fa=%s" % (
        uname,
        pword,
        twofactor,
    )

    ok = login(uname, pword, twofactor, s)
    assert ok, "Login failed with uname=%s, pword=%s, and 2fa=%s" % (
        uname,
        pword,
        twofactor,
    )

    return s


def getQueryIds(s, uname):
    hist = s.get("%s/%s/history" % (SERVICE_ADDR, uname))
    if hist.status_code == 404:
        hist = s.get("%s/history" % (SERVICE_ADDR))

    soup = BeautifulSoup(hist.text, "html.parser")
    queries = soup.findAll(id=re.compile("query\d+"))
    return [i.get("id") for i in queries]


def spellcheck(test_text, uname, pword, twofactor, s=None):
    spellcheck_addr = SERVICE_ADDR + "/spell_check"

    if s == None:
        s = initSession(uname, pword, twofactor)
    spellcheck_args = {}

    form, soup = getSpellcheckForm(s)
    assert form != None, "Spellcheck form is missing id='inputtext'"

    inputs = soup.find_all("input")
    found = False
    for input_field in inputs:
        if input_field.get("id") == "inputtext":
            found = True
    token, remainder = filterXsrfToken(inputs)
    if not found:
        inputs = soup.find_all("textarea")
        for input_field in inputs:
            if input_field.get("id") == "inputtext":
                found = True
                remainder.append(input_field)

    if token is not None:
        xsrf_name = token.get("name")
        spellcheck_args[xsrf_name] = token.get("value")

    for i in remainder:
        if i.get("id") == "inputtext":
            spellcheck_args[i.get("name")] = test_text
        else:
            try:
                spellcheck_args[i.get("name")] = i.get("value")
            except:
                spellcheck_args[i.get("name")] = test_text

    sc_method = form.get("method", "post").lower()

    if sc_method == "post":
        r = s.post(spellcheck_addr, spellcheck_args)
    elif sc_method == "get":
        r = s.request(sc_method, spellcheck_addr)

    return r.text
