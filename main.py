#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import ssl

import sys
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP

from server import ExampleHandler


__version__ = '0.0.1'
__author__ = "Denys Ivanets"
__email__ = "mail@denself.me"


logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-7s %(message)s',
    level=logging.DEBUG,
    stream=sys.stdout
)

log = logging.getLogger()


if __name__ == '__main__':
    host = os.getenv('SMTP_HOST', '*')
    port = os.getenv('SMTP_PORT', '25')
    accept_host = os.getenv('ACCEPT_HOST')
    ssl_keys = os.getenv('SSL_KEYS')

    loop = asyncio.get_event_loop()

    handler = ExampleHandler(accept_host)

    ssl_context = None

    if ssl_keys:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(ssl_keys + '.crt', ssl_keys + '.key')

    controller = Controller(handler,
                            hostname=host,
                            port=port)

    controller.factory = lambda: SMTP(handler,
                                      enable_SMTPUTF8=True,
                                      tls_context=ssl_context)
    controller.start()

    log.info("SMTP server started on %s:%s", host, port)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        controller.stop()
        loop.stop()
        loop.close()
