#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# S/MIME unit tests
#
# This file is part of kryptomime, a Python module for email kryptography.
# Copyright © 2013,2014 Thomas Tanner <tanner@gmx.net>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the included LICENSE file for details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# For more details see the file COPYING.

from pytest import fixture, mark, raises

from kryptomime import KeyMissingError
from kryptomime.mail import create_mail, protect_mail
from kryptomime.smime import OpenSMIME, Certificate, PrivateKey, MemoryKeyStore, OpenSSL, OpenSSL_CA

import email.mime.text

from conftest import sender, receiver
from test_openssl import x509keys, openssl

passphrase='mysecret'
attachment = email.mime.text.MIMEText('some\nattachment')
msg = create_mail(sender,receiver,'subject','body\nmessage')
msg.epilogue=''
msgatt = create_mail(sender,receiver,'subject','body\nmessage',attach=[attachment])
msgrev = create_mail(receiver,sender,'subject','body\nmessage')
msgself = create_mail(sender,sender,'subject','body\nmessage')
prot = protect_mail(msg,linesep='\r\n')
protatt = protect_mail(msgatt,linesep='\r\n')

def compare_mail(a,b):
    if type(a)==str: return a==b
    assert a.is_multipart() == b.is_multipart()
    #from kryptomime.mail import ProtectedMessage
    #assert isinstance(a,ProtectedMessage)==isinstance(b,ProtectedMessage)
    # todo headers
    if a.is_multipart():
        for i in range(len(a.get_payload())):
            ap = a.get_payload(i)
            bp = b.get_payload(i)
            assert ap.as_string() == bp.as_string()
    else:
        assert a.get_payload() == b.get_payload()

@fixture(scope='module')
def smimesender(x509keys,openssl):
    return (OpenSMIME(openssl=openssl,default_key=x509keys[0]),x509keys[0].cacerts)

@fixture(scope='module')
def smimereceiver(x509keys,openssl):
    return (OpenSMIME(openssl=openssl,default_key=x509keys[1]),x509keys[0].cacerts)

@mark.parametrize("attach", [False,True])
def test_sign(x509keys, attach, smimesender, smimereceiver):
    id1, cacert1 = smimesender
    id2, cacert2 = smimereceiver
    mail = protatt if attach else prot
    sgn = id1.sign(mail)
    vfy, signer, valid = id2.verify(sgn,cacerts=cacert1)
    assert valid and x509keys[0].cert == signer
    compare_mail(mail,vfy)

@mark.parametrize("sign", [False,True])
def test_encrypt(x509keys, sign, smimesender, smimereceiver):
    id1, cacert1 = smimesender
    id2, cacert2 = smimereceiver
    enc = id1.encrypt(protatt,[x509keys[1]],sign=sign, verify=True)
    dec = id2.decrypt(enc,verify=sign,cacerts=cacert1)
    if sign:
        dec, signer, valid = dec
        assert valid and x509keys[0].cert == signer
    compare_mail(protatt,dec)
