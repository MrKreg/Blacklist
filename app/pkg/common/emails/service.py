from pyquery import PyQuery
from django.conf import settings

from app.pkg.common.emails.mail import send_mail
from app.pkg.common.emails.messages import MessageNotification


class EmailService(object):

    @staticmethod
    def get_plain_text(message):
        html = PyQuery(message)
        body = html('body')
        if body:
            return body.text()
        return html.text()

    def _send_email(self, subject, message, email, attachments=None):
        from_email = settings.DEFAULT_FROM_EMAIL
        plain_message = self.get_plain_text(message)

        send_mail(subject, plain_message, from_email, [email],
                  html_message=message, attachments=attachments)

    def _process_email(self, email, msg, subject='', attachments=None):
        message = self._get_message(msg)
        sbj = self._get_subject(msg, subject)
        self._send_email(sbj, message, email, attachments=attachments)

    def send_to_email(self, msg, email, subject='', attachments=None):
        self._process_email(email, msg, subject, attachments)

    @staticmethod
    def _get_message(email_message):
        if isinstance(email_message, MessageNotification):
            content = email_message.get_content()
        else:
            content = email_message
        return content.replace('\n', '')

    @staticmethod
    def _get_subject(email_message, subject=''):
        if isinstance(email_message, MessageNotification):
            return email_message.get_subject()
        return subject


class EmailNotification(object):
    service = EmailService()

    template_name = NotImplemented
    subject = NotImplemented

    @classmethod
    def get_message_class(cls):
        return type('Message', (MessageNotification, ), {
            'template_name': cls.template_name,
            'subject': cls.subject
        })

    @classmethod
    def get_message(cls, **context_data):
        message_class = cls.get_message_class()
        return message_class(**context_data)

    @classmethod
    def get_context(cls, **kwargs):
        return kwargs

    @classmethod
    def send_to_email(cls, email, attachments=None, **kwargs):
        print('sending')
        message = cls.get_message(**cls.get_context(**kwargs))
        cls.service.send_to_email(message, email, attachments=attachments)
