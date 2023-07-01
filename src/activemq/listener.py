import stomp

from src.activemq.cache.cache import ActivemqMessageCache

class ReplyListener(stomp.ConnectionListener):
    def __init__(self) -> None:
        super().__init__()
        self.activemq_message_cache = ActivemqMessageCache()        
