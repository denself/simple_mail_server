import email
import logging
from email.message import Message

import dkim
import spf
from aiosmtpd.smtp import Envelope, Session, SMTP

from tools import message_to_display

log = logging.getLogger("smtphandler")

test_results = ['FAIL', 'PASS']


class ExampleHandler:

    def __init__(self,
                 verify_dkim: bool = False,
                 verify_spf: bool = False):
        self.verify_dkim = verify_dkim
        self.verify_spf = verify_spf

    async def handle_MAIL(self,
                          server: SMTP,
                          session: Session,
                          envelope: Envelope,
                          address: str,
                          mail_options: list):

        ip = session.peer[0]
        result, description = spf.check2(ip, address, session.host_name)

        log.info("SPF: %s, %s", result, description)

        if self.verify_spf and result != 'pass':
            return '550 SPF validation failed'

        envelope.mail_from = address
        envelope.mail_options.extend(mail_options)

        return '250 OK'

    async def handle_RCPT(self,
                          server: SMTP,
                          session: Session,
                          envelope: Envelope,
                          address: str,
                          rcpt_options: list):
        # Accept all incoming mail for now
        # if not address.endswith('@example.com'):
        #     return '550 not relaying to that domain'
        log.debug("Handle RCPT for %s", address)
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self,
                          server: SMTP,
                          session: Session,
                          envelope: Envelope):

        valid_dkim = dkim.verify(envelope.content)
        log.info("DKIM: %s", test_results[valid_dkim])

        message: Message = email.message_from_bytes(envelope.content)

        log.info('From: %s', message['From'])
        log.info('To: %s', message['To'])
        log.info('Subject: %s', message['Subject'])
        log.info('Message data:\n%s', message_to_display(message))

        if self.verify_dkim and not valid_dkim:
            return '550 DKIM validation failed'

        return '250 Message accepted for delivery'
