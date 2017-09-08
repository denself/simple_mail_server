#!/usr/bin/env python3.6
import asyncio
import logging

import os

import sys
from aiosmtpd.controller import Controller

from server import ExampleHandler


logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-7s %(message)s',
    level=logging.DEBUG,
    stream=sys.stdout
)

log = logging.getLogger()


if __name__ == '__main__':
    host = os.getenv('SMTP_HOST', '*')
    port = os.getenv('SMTP_PORT', '25')

    loop = asyncio.get_event_loop()
    controller = Controller(ExampleHandler(), hostname=host, port=port)
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
