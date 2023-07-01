import email
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import stomp
import stomp.utils


class NotificationMsg():
    def __init__(
        self,
        send_email: bool = True,
        send_whatsapp: bool = False,
        send_sms: bool = False,
        email: str = None,
        subject: str = None,
        message: str = None,
        phone_number: str = None,
        ) -> None:
        self.send_email = send_email
        self.send_whatsapp = send_whatsapp
        self.send_sms = send_sms
        self.email = email
        self.subject = subject
        self.message = message
        self.phone_number = phone_number
            
    def serialize(self):
        mime_multipart = MIMEMultipart()
        part = MIMEText(str(self.send_email))
        part.add_header('Content-ID', 'send_email')
        mime_multipart.attach(part)
        part = MIMEText(str(self.send_whatsapp))
        part.add_header('Content-ID', 'send_whatsapp')
        mime_multipart.attach(part)
        part = MIMEText(str(self.send_sms))
        part.add_header('Content-ID', 'send_sms')
        mime_multipart.attach(part)
        part = MIMEText(self.email)
        part.add_header('Content-ID', 'email')
        mime_multipart.attach(part)
        part = MIMEText(self.subject)
        part.add_header('Content-ID', 'subject')
        mime_multipart.attach(part)
        part = MIMEText(self.message)
        part.add_header('Content-ID', 'message')
        mime_multipart.attach(part)
        if self.phone_number:
            part = MIMEText(self.phone_number)
            part.add_header('Content-ID', 'phone_number')
            mime_multipart.attach(part)
        return mime_multipart.as_string()
    
    def deserialize(self, frame: stomp.utils.Frame):
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'send_email':
                self.send_email = part.get_payload(decode=False) == 'True'
            elif part.get('Content-ID') == 'send_whatsapp':
                self.send_whatsapp = part.get_payload(decode=False) == 'True'
            elif part.get('Content-ID') == 'send_sms':
                self.send_sms = part.get_payload(decode=False) == 'True'
            elif part.get('Content-ID') == 'email':
                self.email = part.get_payload(decode=False)
            elif part.get('Content-ID') == 'subject':
                self.subject = part.get_payload(decode=False)
            elif part.get('Content-ID') == 'message':
                self.message = part.get_payload(decode=False)
            elif part.get('Content-ID') == 'phone_number':
                self.phone_number = part.get_payload(decode=False)

    def __eq__(self, msg):
        return isinstance(msg, NotificationMsg) and \
            self.send_email == msg.send_email and \
            self.send_whatsapp == msg.send_whatsapp and \
            self.send_sms == msg.send_sms and \
            self.email == msg.email and \
            self.subject == msg.subject and \
            self.message == msg.message and \
            self.phone_number == msg.phone_number

    def __str__(self):
        return f'''NotificationMsg:
        send_email: {self.send_email}
        send_whatsapp: {self.send_whatsapp}
        send_sms: {self.send_sms}
        email: {self.email}
        subject: {self.subject}
        message: {self.message}
        phone_number: {self.phone_number}
        '''