import email
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET
from src.activemq.cache.message import CachedMessage
import stomp.utils


class ConvertImageMsg(CachedMessage):
    def __init__(
        self, 
        correlation_id: str = None,
        image_data: bytes = None, 
        image_format: str = None
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.image_data = image_data
        self.image_format = image_format
        
    def serialize(self) -> str:
        mime_multipart = MIMEMultipart()
        part = MIMEImage(self.image_data)
        part.add_header('Content-ID', 'data')
        mime_multipart.attach(part)
        part = MIMEText(self.image_format)
        part.add_header('Content-ID', 'image_format')
        mime_multipart.attach(part)
        return mime_multipart.as_string()

    def deserialize(self, frame: stomp.utils.Frame) -> None:
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'data':
                self.image_data = part.get_payload(decode=True)
            elif part.get('Content-ID') == 'image_format':
                self.image_format = part.get_payload(decode=True)
        self.correlation_id = frame.headers.get('correlation_id')
        

    def __str__(self):
        return f'''ConvertImageMsg:
        correlation_id: {self.correlation_id},
        image_format: {self.image_format}
        '''


class ConvertImageReplyMsg(CachedMessage):
    def __init__(
        self, 
        correlation_id: str = None, 
        image_data: bytes = None
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.image_data = image_data
        
    def serialize(self):
        mime_multipart = MIMEMultipart()
        part = MIMEImage(self.image_data)
        part.add_header('Content-ID', 'data')
        mime_multipart.attach(part)
        return mime_multipart.as_string()
        
    def deserialize(self, frame: stomp.utils.Frame):
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'data':
                self.image_data = part.get_payload(decode=True)
        self.correlation_id = frame.headers.get('correlation_id')
        
    def __eq__(self, msg):
        return isinstance(msg, ConvertImageReplyMsg) \
            and self.correlation_id == msg.correlation_id \
                and self.image_data == msg.image_data

    def __str__(self):
        return f'''ConvertImageReplyMsg:
        correlation_id: {self.correlation_id}'''