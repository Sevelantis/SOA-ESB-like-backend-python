import logging
from io import BytesIO

import stomp
import stomp.utils
from PIL import Image

from src.activemq.cache.cache import ActivemqMessageCache
from src.activemq.listener import ReplyListener
from src.conversion.message import ConvertImageReplyMsg


class ConvertImageReplyListener(ReplyListener):
    def __init__(self) -> None:
        ReplyListener.__init__(self)
        
    def on_message(self, frame: stomp.utils.Frame):
        msg = ConvertImageReplyMsg()
        msg.deserialize(frame=frame)
        # local debug
        # converted_image = Image.open(BytesIO(msg.image_data))
        # converted_image.show()
        
        self.activemq_message_cache.push(msg=msg)
