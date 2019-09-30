import requests
from bs4 import BeautifulSoup

SERVICE_ADDR = "http://127.0.0.1:5000"
REPORTER_ADDR = "http://127.0.0.1:31337"


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
        input_name = soup.get("name").lower()

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

    spellcheck = BeautifulSoup(r.text, "html.parser")
    input_form = soup.find("form", id="inputtext")
    return input_form


def registerAccount(uname, pword, twofactor, session=None):
    addr = SERVICE_ADDR + "/register"
    if session is None:
        session = requests.Session()

    test_creds = {"uname": uname, "pword": pword, "2fa": twofactor}
    r = s.post(addr, data=test_creds)
    success = getElementById(r.text, "success")
    return "success" in success.text


def login(uname, pword, twofactor, session=None):
    addr = SERVICE_ADDR + "/login"
    if session is None:
        session = requests.Session()

    test_creds = {"uname": uname, "pword": pword, "2fa": twofactor}
    r = s.post(addr, data=test_creds)
    success = getElementById(r.text, "result")
    return "success" in success.text


def initSession(uname, pword, twofactor):
    s = requests.Session()
    ok = registerAccount(uname, pword, twofactor, s)
    assert ok

    ok = login(uname, pword, twofactor, s)
    assert ok

    return s


def spellcheck(test_text, uname, pword, twofactor):
    s = init_test_session(uname, pword, twofactor)
    spellcheck_args = {}

    form = getSpellcheckForm(s)
    inputs = input_form.find_all("input")
    token, remainder = filterXsrfToken(inputs)

    if token is not None:
        xsrf_name = token.get("name")
        spellcheck_args[xsrf_name] = token.get_text()

    for i in remainder:
        spellcheck_args[i.get("name")] = test_text

    sc_method = form.get("method")

    if sc_method == "post":
        r = s.request(sc_method, spellcheck_addr)
    elif sc_method == "get":
        r = s.request(sc_method, spellcheck_addr)
