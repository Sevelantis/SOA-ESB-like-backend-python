import stomp
import stomp.utils
import logging
from src.activemq.cache.cache import ActivemqMessageCache
from src.activemq.listener import ReplyListener

from src.s3_connector.message import GetImageReplyMsg, StoreImageReplyMsg


class GetImageReplyListener(ReplyListener):
    def __init__(self) -> None:
        ReplyListener.__init__(self)
        
    def on_message(self, frame: stomp.utils.Frame):
        msg = GetImageReplyMsg()
        msg.deserialize(frame=frame)
        self.activemq_message_cache.push(msg=msg)
    
class StoreImageReplyListener(ReplyListener):
    def __init__(self) -> None:
        ReplyListener.__init__(self)
        
    def on_message(self, frame: stomp.utils.Frame):
        msg = StoreImageReplyMsg()
        msg.deserialize(frame=frame)
        self.activemq_message_cache.push(msg=msg)
