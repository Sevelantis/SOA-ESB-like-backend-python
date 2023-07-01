from fastapi import Depends
import stomp.connect as connect
from src.activemq.manager import ActivemqWorkerManager
from src.activemq.cache.cache import ActivemqMessageCache
from src.activemq.cache.manager import ActivemqCacheManager
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, ActivemqWorkerFactory
import src.config as config

def connection() -> connect.StompConnection11:
    return ActiveMqConnectionFactory.create_connection(
        broker_host=config.ACTIVEMQ_HOST,
        broker_port=config.ACTIVEMQ_PORT,
        broker_username=config.ACTIVEMQ_USERNAME,
        broker_password=config.ACTIVEMQ_PASSWORD,
        listener=None
    )


def activemq_dispatcher(
    connection: connect.StompConnection11 = Depends(connection),
    ) -> ActivemqDispatcher:
    
    return ActivemqDispatcher(conn=connection)

def activemq_message_cache() -> ActivemqMessageCache:
    return ActivemqMessageCache()

def activemq_cache_manager(
    activemq_message_cache: ActivemqMessageCache = Depends(activemq_message_cache)
    ) -> ActivemqCacheManager:
    return ActivemqCacheManager(
        activemq_message_cache=activemq_message_cache
    )
