#!/usr/bin/env python3.6
import asyncio

import os
from aiosmtpd.controller import Controller

from server import ExampleHandler


if __name__ == '__main__':
    host = os.getenv('SMTP_HOST', '::1')
    port = os.getenv('SMTP_PORT', 8025)

    loop = asyncio.get_event_loop()

    controller = Controller(ExampleHandler(), loop, host, port)
    controller.start()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        controller.stop()
        loop.stop()
        loop.close()
