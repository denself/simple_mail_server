#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import pytest
from aiosmtpd.smtp import Envelope, SMTP, Session

from server import ExampleHandler


class TestExampleHandler:

    def setup_method(self, method):
        self.handler = ExampleHandler()
        self.envelope = Envelope()
        self.envelope.content = b"""From: Cate Person <cate@example.com>
To: Dave Person <dave@example.com>
Subject: A test
Message-ID: <bee>

Hi Dave, this is Cate."""
        self.server = SMTP(self.handler)

    @pytest.mark.asyncio
    async def test_handle_DATA(self):
        server = SMTP(self.handler)
        response = await self.handler.handle_DATA(
            self.server,
            Session(server.loop),
            self.envelope
        )
        assert response == '250 Message accepted for delivery'

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
