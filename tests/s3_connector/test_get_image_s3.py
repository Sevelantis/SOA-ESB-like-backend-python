import pytest
import stomp
import stomp.utils
from src.activemq.cache.utils import CorrelationIdGenerator
from src.activemq.utils import SubIdGenerator
from src.activemq.worker import ActiveMqWorker
from src.activemq.manager import ActivemqWorkerManager
from src.s3_connector.message import GetImageMsg, GetImageReplyMsg, StoreImageMsg
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, ActivemqWorkerFactory, MessageFactory
import src.config as config
import logging
import time
from tests.test_base import *

@pytest.fixture()
def mocked_get_image_worker(
    send_conn: stomp.connect.StompConnection11,
    mocked_get_image_reply_msg: GetImageReplyMsg
    ) -> ActiveMqWorker:
    class MockedGetImageListener(stomp.ConnectionListener):
        def __init__(self) -> None:
            super().__init__()
        def on_message(self, frame: stomp.utils.Frame):
            msg = GetImageMsg()
            msg.deserialize(frame=frame)
            send_conn.send(
                destination=config.ACTIVEMQ_GET_IMAGE_REPLY_QUEUE,
                body=mocked_get_image_reply_msg.serialize(),
                headers={
                    'content-type': 'multipart/mixed',
                    'correlation_id': mocked_get_image_reply_msg.correlation_id
                    }
            )
            
    return ActiveMqWorker(
        connection=ActiveMqConnectionFactory.create_connection(
            listener=MockedGetImageListener()
        ),
        sub_id=SubIdGenerator.generate_next(),
        queue=config.ACTIVEMQ_GET_IMAGE_QUEUE
    )
    
@pytest.fixture()
def get_image_reply_worker():
    return ActivemqWorkerFactory().create_get_image_reply_worker()


@pytest.fixture()
def activemq_worker_manager(
    mocked_get_image_worker: ActiveMqWorker,
    get_image_reply_worker: ActiveMqWorker,
):
    return ActivemqWorkerManager(workers=[
            mocked_get_image_worker,
            get_image_reply_worker
    ])
    
@pytest.fixture()
def correlation_id() -> str:
    # return CorrelationIdGenerator.generate()
    return 'CorrelationIdGenerator.generate()'

@pytest.fixture()
def mocked_get_image_msg(
    message_factory: MessageFactory,
    correlation_id: str
    ) -> StoreImageMsg:
    return message_factory.create_get_image_message(
        filename='raccoon.png',
        correlation_id=correlation_id
    )
    
    
@pytest.fixture()
def mocked_get_image_reply_msg(
    correlation_id: str
    ) -> GetImageReplyMsg:
    return GetImageReplyMsg(
        url='www.thisismydownloadsuperurl.pls/raccoon.png',
        correlation_id=correlation_id
        )


def test_get_image(
    activemq_dispatcher: ActivemqDispatcher, 
    activemq_worker_manager: ActivemqWorkerManager,
    mocked_get_image_msg: GetImageMsg,
    mocked_get_image_reply_msg: GetImageReplyMsg,
    activemq_cache_manager: ActivemqCacheManager
    ):
    assert type(activemq_dispatcher) == ActivemqDispatcher
    assert type(activemq_worker_manager) == ActivemqWorkerManager
    assert type(mocked_get_image_msg) == GetImageMsg
    assert type(mocked_get_image_reply_msg) == GetImageReplyMsg
    assert type(activemq_cache_manager) == ActivemqCacheManager
    
    activemq_worker_manager.submit_threadpool()

    activemq_dispatcher.send_get_image_message(
        msg=mocked_get_image_msg
        )
    
    time.sleep(3)
    
    await_msg = activemq_cache_manager.await_reply_message(
        correlation_id=mocked_get_image_msg.correlation_id
        )
    assert await_msg == mocked_get_image_reply_msg
    
    activemq_worker_manager.stop_threadpool()
