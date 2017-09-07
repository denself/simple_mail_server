import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import Envelope, Session


class ExampleHandler:
    async def handle_RCPT(self,
                          server,
                          session: Session,
                          envelope: Envelope,
                          address: str,
                          rcpt_options):
        if not address.endswith('@example.com'):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self,
                          server,
                          session,
                          envelop: Envelope):
        content = envelop.content.decode("utf8", errors="replace")
        print(f'Message from {envelop.mail_from}')
        print(f'Message for {envelop.rcpt_tos}')
        print(f'Message data:\n{content}')
        print('End of message')
        return '250 Message accepted for delivery'


if __name__ == '__main__':
    controller = Controller(ExampleHandler(), ready_timeout=5)
    controller.start()
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        controller.stop()
        loop.stop()
        loop.close()
