# -*- coding: utf-8 -*-
from base64 import b64decode
import email
import imaplib
import settings as config

__author__ = 'whoami'
__version__ = '0.0.1'
__date__ = '24.02.16 22:40'
__description__ = """
Работа с почтой.
"""


class EmailBox(imaplib.IMAP4_SSL):
    __server = config.imap_server
    __port = config.imap_port

    def __init__(self):
        super().__init__(self.__server, self.__port)

    @staticmethod
    def get_first_text_block(email_message_instance):
        body = b''

        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    try:
                        body += b64decode(part.get_payload())
                    except Exception:
                        pass
            return body
        elif maintype == 'text':
            body += b64decode(email_message_instance.get_payload())
            return body

    def get_emails(self, user, password):
        try:
            self.login(user, password)
        except Exception as e:
            print(e)

        self.select()

        typ, data = self.search(None, 'ALL')
        id_list = data[0].split()
        for num in id_list[::-1]:
            try:
                typ, data = self.fetch(num, '(RFC822)')
                raw_mail = data[0][1]
                email_message = email.message_from_string(raw_mail.decode('utf-8'))
                yield self.get_first_text_block(email_message)
            except Exception:
                continue

    def __del__(self):
        if self.state == 'SELECTED':
            self.close()
        self.logout()
