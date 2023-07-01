import email
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import stomp
import stomp.utils
from src.activemq.cache.message import CachedMessage

class StoreImageMsg(CachedMessage):
    def __init__(
        self, 
        correlation_id: str = None,
        filename: str = None, 
        image_data: bytes = None
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.filename = filename
        self.image_data = image_data
            
    def serialize(self):
        mime_multipart = MIMEMultipart()
        part = MIMEImage(self.image_data)
        part.add_header('Content-ID', 'data')
        mime_multipart.attach(part)
        part = MIMEText(self.filename)
        part.add_header('Content-ID', 'filename')
        mime_multipart.attach(part)
        return mime_multipart.as_string()  
    
    def deserialize(self, frame: stomp.utils.Frame):
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'data':
                self.image_data = part.get_payload(decode=True)
            elif part.get('Content-ID') == 'filename':
                self.image_format = part.get_payload(decode=False)
        self.correlation_id = frame.headers.get('correlation_id')


    def __str__(self):
        return f'''StoreImageMsg:
        correlation_id: {self.correlation_id},
        filename: {self.filename}
        '''

class StoreImageReplyMsg(CachedMessage):
    def __init__(
        self,
        correlation_id: str = None,
        url: str = None
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.url = url
        self.correlation_id = correlation_id
    
    def serialize(self):
        mime_multipart = MIMEMultipart()
        part = MIMEText(self.url)
        part.add_header('Content-ID', 'url')
        mime_multipart.attach(part)
        return mime_multipart.as_string()  
    
    def deserialize(self, frame: stomp.utils.Frame):
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'url':
                self.url = part.get_payload(decode=False)
        self.correlation_id = frame.headers.get('correlation_id')
        
    def __eq__(self, msg):
        return isinstance(msg, StoreImageReplyMsg) \
            and self.correlation_id == msg.correlation_id \
                and self.url == msg.url

    def __str__(self):
        return f'''StoreImageReplyMsg:
        correlation_id: {self.correlation_id},
        url: {self.url}
        '''


class GetImageMsg(CachedMessage):
    def __init__(
        self,
        correlation_id: str = None,
        filename: str = None
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.filename = filename
            
    def serialize(self):
        mime_multipart = MIMEMultipart()
        part = MIMEText(self.filename)
        part.add_header('Content-ID', 'filename')
        mime_multipart.attach(part)
        return mime_multipart.as_string() 
    
    def deserialize(self, frame: stomp.utils.Frame):
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'filename':
                self.url = part.get_payload(decode=False)
        self.correlation_id = frame.headers.get('correlation_id')


    def __str__(self):
        return f'''GetImageMsg:
        correlation_id: {self.correlation_id},
        filename: {self.filename}
        '''

class GetImageReplyMsg(CachedMessage):
    def __init__(
        self,
        correlation_id: str = None,
        url: str = None
        ) -> None:
        CachedMessage.__init__(self, correlation_id=correlation_id)
        self.url = url
            
    def serialize(self):
        mime_multipart = MIMEMultipart()
        part = MIMEText(self.url)
        part.add_header('Content-ID', 'url')
        mime_multipart.attach(part)
        return mime_multipart.as_string() 
    
    def deserialize(self, frame: stomp.utils.Frame):
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'url':
                self.url = part.get_payload(decode=False)
        self.correlation_id = frame.headers.get('correlation_id')
    
    def __eq__(self, msg):
        return isinstance(msg, GetImageReplyMsg) \
            and self.correlation_id == msg.correlation_id \
                and self.url == msg.url

    def __str__(self):
        return f'''GetImageReplyMsg:
        correlation_id: {self.correlation_id},
        url: {self.url}
        '''

class DeleteImageMsg():
    def __init__(
        self,
        filename: str = None
        ) -> None:
        self.filename = filename
            
    def serialize(self):
        mime_multipart = MIMEMultipart()
        part = MIMEText(self.filename)
        part.add_header('Content-ID', 'filename')
        mime_multipart.attach(part)
        return mime_multipart.as_string() 
    
    def deserialize(self, frame: stomp.utils.Frame):
        mime_message: MIMEMessage = email.message_from_string(frame.body)
        for part in mime_message.walk():
            if part.get('Content-ID') == 'filename':
                self.filename = part.get_payload(decode=False)

    def __eq__(self, msg):
        return isinstance(msg, DeleteImageMsg) \
                and self.filename == msg.filename

    def __str__(self):
        return f'''DeleteImageMsg:
        filename: {self.filename},
        '''