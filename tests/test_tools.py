#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import email

from tools import message_to_display


def test_message_to_display_plain():
    mail = email.message_from_bytes(b"""\
From: Cate Person <cate@example.com>
To: Dave Person <dave@example.com>
Subject: A test
Message-ID: <bee>

Hi Dave, this is Cate.
""")

    result = message_to_display(mail)
    assert result == """\
Content-type: text/plain
Hi Dave, this is Cate.

****************************************************************************
"""


def test_message_to_display_multipart():
    mail = email.message_from_bytes(b"""\
From: Cate Person <cate@example.com>
To: Dave Person <dave@example.com>
Subject: A test
Message-ID: <bee>
Content-Type: multipart/alternative; boundary="001a114a16900f66a40558e72324"

--001a114a16900f66a40558e72324
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

Hi Dave, this is Cate.

--001a114a16900f66a40558e72324
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div dir=3D"ltr">Hi Dave, this is Cate</div>

--001a114a16900f66a40558e72324--""")

    result = message_to_display(mail)
    assert result == """\
Content-type: text/plain
Hi Dave, this is Cate.

****************************************************************************
Content-type: text/html
<div dir=3D"ltr">Hi Dave, this is Cate</div>

****************************************************************************
"""
