from src.activemq.cache.message import CachedMessage
import threading
    
class ActivemqMessageCache:
    _instance = None
    _lock = threading.Lock()
    cache = {}
        
    def __new__(cls):
        if cls._instance is None: 
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def push(cls, msg: CachedMessage) -> None:
        cls.cache[msg.correlation_id] = msg
        x = -1
    
    @classmethod
    def pop(cls, correlation_id: str) -> None:
        del cls.cache[correlation_id]
    
    @classmethod
    def get(cls, correlation_id: str) -> CachedMessage:
        if correlation_id in cls.cache:
            return cls.cache[correlation_id]
        return None
