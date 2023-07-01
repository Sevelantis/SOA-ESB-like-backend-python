import time
import pytest
import stomp
import stomp.utils
from src.activemq.utils import SubIdGenerator
from src.activemq.worker import ActiveMqWorker
from src.activemq.manager import ActivemqWorkerManager
from src.s3_connector.message import DeleteImageMsg, GetImageMsg, GetImageReplyMsg, StoreImageMsg, StoreImageReplyMsg
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, ActivemqWorkerFactory, MessageFactory
from src.s3_connector.listener import GetImageReplyListener, StoreImageReplyListener
import src.config as config
import logging
from tests.test_base import *

s3_received_delete_msg   = None

@pytest.fixture()
def mocked_delete_image_worker() -> ActiveMqWorker:
    class MockedDeleteImageListener(stomp.ConnectionListener):
        def __init__(self) -> None:
            super().__init__()
        def on_message(self, frame: stomp.utils.Frame):
            msg = DeleteImageMsg()
            msg.deserialize(frame=frame)
            global s3_received_delete_msg
            s3_received_delete_msg = msg
            
    return ActiveMqWorker(
        connection=ActiveMqConnectionFactory.create_connection(
            listener=MockedDeleteImageListener()
        ),
        sub_id=SubIdGenerator.generate_next(),
        queue=config.ACTIVEMQ_DELETE_IMAGE_QUEUE
    )
    
@pytest.fixture()
def activemq_worker_manager(
    mocked_delete_image_worker: ActiveMqWorker
):
    return ActivemqWorkerManager(workers=[
            mocked_delete_image_worker
    ])
    
@pytest.fixture()
def mocked_delete_image_msg(
    message_factory: MessageFactory
    ) -> DeleteImageMsg:
    return message_factory.create_delete_image_message(
        filename='raccoon.png'
    )

def test_delete_image(
    activemq_dispatcher: ActivemqDispatcher, 
    activemq_worker_manager: ActivemqWorkerManager,
    mocked_delete_image_msg: DeleteImageMsg,
    activemq_cache_manager: ActivemqCacheManager
    ):
    assert type(activemq_dispatcher) == ActivemqDispatcher
    assert type(activemq_worker_manager) == ActivemqWorkerManager
    assert type(mocked_delete_image_msg) == DeleteImageMsg
    assert type(activemq_cache_manager) == ActivemqCacheManager
    
    activemq_worker_manager.submit_threadpool()

    activemq_dispatcher.send_delete_image_message(
        msg=mocked_delete_image_msg
        )
    
    time.sleep(3)
    
    assert s3_received_delete_msg == mocked_delete_image_msg
    
    activemq_worker_manager.stop_threadpool()
