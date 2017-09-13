#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import pytest
from aiosmtpd.smtp import Envelope, SMTP, Session

from server import ExampleHandler


class TestExampleHandler:

    def setup_method(self, method):
        self.handler = ExampleHandler(verify_spf=True)
        self.envelope = Envelope()
        self.envelope.content = b"""From: Cate Person <cate@gmail.com>
To: Dave Person <dave@gmail.com>
Subject: A test
Message-ID: <bee>

Hi Dave, this is Cate."""
        self.server = SMTP(self.handler)

    @pytest.mark.asyncio
    async def test_handle_MAIL_spf(self):
        server = SMTP(self.handler)
        session = Session(server.loop)
        session.peer = ['209.85.220.69', 65000]
        session.host_name = 'gmail.com'
        response = await self.handler.handle_MAIL(
            self.server,
            session,
            Envelope(),
            'cate@gmail.com',
            []
        )
        assert response == '250 OK'

    @pytest.mark.asyncio
    async def test_handle_MAIL_no_spf(self):
        server = SMTP(self.handler)
        session = Session(server.loop)
        session.peer = ['127.0.0.1', 65000]
        response = await self.handler.handle_MAIL(
            self.server,
            session,
            self.envelope,
            'cate@gmail.com',
            []
        )
        assert response == '550 SPF validation failed'

    @pytest.mark.asyncio
    async def test_handle_DATA(self):
        self.handler.verify_dkim = False
        server = SMTP(self.handler)
        response = await self.handler.handle_DATA(
            self.server,
            Session(server.loop),
            self.envelope
        )
        assert response == '250 Message accepted for delivery'

    @pytest.mark.asyncio
    async def test_handle_DATA_fail_dkim(self):
        self.handler.verify_dkim = True
        server = SMTP(self.handler)
        response = await self.handler.handle_DATA(
            self.server,
            Session(server.loop),
            self.envelope
        )
        assert response == '550 DKIM validation failed'

    @pytest.mark.asyncio
    async def test_handle_RCPT(self):
        # In this test, the message data comes in as bytes.
        server = SMTP(self.handler)

        response = await self.handler.handle_RCPT(
            self.server,
            Session(server.loop),
            self.envelope,
            '',
            []
        )
        assert response == '250 OK'
