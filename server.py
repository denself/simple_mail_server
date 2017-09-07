from aiosmtpd.smtp import Envelope, Session, SMTP


class ExampleHandler:
    async def handle_RCPT(self,
                          server: SMTP,
                          session: Session,
                          envelope: Envelope,
                          address: str,
                          rcpt_options: list):
        if not address.endswith('@example.com'):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self,
                          server: SMTP,
                          session: Session,
                          envelop: Envelope):
        content = envelop.content.decode("utf8", errors="replace")
        print(f'Message from {envelop.mail_from}')
        print(f'Message for {envelop.rcpt_tos}')
        print(f'Message data:\n{content}')
        print('End of message')
        return '250 Message accepted for delivery'
