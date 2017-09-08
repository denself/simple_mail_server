import logging

from aiosmtpd.smtp import Envelope, Session, SMTP


log = logging.getLogger("smtphandler")


class ExampleHandler:
    async def handle_RCPT(self,
                          server: SMTP,
                          session: Session,
                          envelope: Envelope,
                          address: str,
                          rcpt_options: list):
        # Accept all incoming mail for now
        # if not address.endswith('@example.com'):
        #     return '550 not relaying to that domain'
        log.info("Handle RCPT for %s", address)
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self,
                          server: SMTP,
                          session: Session,
                          envelop: Envelope):
        content = envelop.content
        log.debug('Message from %s', envelop.mail_from)
        log.debug('Message for %s', envelop.rcpt_tos)
        log.debug('Message data:\n%s\n%s', content, '*'*20)
        return '250 Message accepted for delivery'
