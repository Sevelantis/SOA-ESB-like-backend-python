import pytest
import stomp
import stomp.utils
from src.activemq.cache.utils import CorrelationIdGenerator
from src.activemq.utils import SubIdGenerator
from src.activemq.worker import ActiveMqWorker
from src.activemq.manager import ActivemqWorkerManager
from src.s3_connector.message import GetImageMsg, StoreImageMsg, StoreImageReplyMsg
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, ActivemqWorkerFactory, MessageFactory
from src.s3_connector.listener import GetImageReplyListener, StoreImageReplyListener
import src.config as config
import logging
from tests.test_base import *

@pytest.fixture()
def mocked_store_image_worker(
    send_conn: stomp.connect.StompConnection11,
    mocked_store_image_reply_msg: StoreImageReplyMsg
    ) -> ActiveMqWorker:
    class MockedStoreImageListener(stomp.ConnectionListener):
        def __init__(self) -> None:
            super().__init__()
        def on_message(self, frame: stomp.utils.Frame):
            msg = StoreImageMsg()
            msg.deserialize(frame=frame)
            # for debug
            # with open('sample_images/result.jpg', 'wb') as f:
            #     f.write(msg.image_data)
            # send back mocked message
            send_conn.send(
                destination=config.ACTIVEMQ_STORE_IMAGE_REPLY_QUEUE,
                body=mocked_store_image_reply_msg.serialize(),
                headers={
                    'content-type': 'multipart/mixed',
                    'correlation_id': mocked_store_image_reply_msg.correlation_id
                    }
            )
            
    return ActiveMqWorker(
        connection=ActiveMqConnectionFactory.create_connection(
            listener=MockedStoreImageListener()
        ),
        sub_id=SubIdGenerator.generate_next(),
        queue=config.ACTIVEMQ_STORE_IMAGE_QUEUE
    )
    
@pytest.fixture()
def store_image_reply_worker():
    return ActivemqWorkerFactory().create_store_image_reply_worker()


@pytest.fixture()
def activemq_worker_manager(
    mocked_store_image_worker: ActiveMqWorker,
    store_image_reply_worker: ActiveMqWorker,
):
    return ActivemqWorkerManager(workers=[
            mocked_store_image_worker,
            store_image_reply_worker
    ])

@pytest.fixture()
def correlation_id() -> str:
    return CorrelationIdGenerator.generate()
    
@pytest.fixture()
def mocked_store_image_msg(
    message_factory: MessageFactory,
    mocked_upload_file_png: UploadFile,
    correlation_id: str
    ) -> StoreImageMsg:
    return message_factory.create_store_image_message(
        filename='raccoon_to_store.png',
        image_data=mocked_upload_file_png.file.read(),
        correlation_id=correlation_id
    )
    
    
@pytest.fixture()
def mocked_store_image_reply_msg(
    mocked_upload_file_png: UploadFile,
    correlation_id: str
    ) -> StoreImageReplyMsg:
    return StoreImageReplyMsg(
        url='my_super_url.com/raccoon.png',
        correlation_id=correlation_id
        )


def test_store_image(
    activemq_dispatcher: ActivemqDispatcher, 
    activemq_worker_manager: ActivemqWorkerManager,
    mocked_store_image_msg: StoreImageMsg,
    mocked_store_image_reply_msg: StoreImageReplyMsg,
    activemq_cache_manager: ActivemqCacheManager
    ):
    assert type(activemq_dispatcher) == ActivemqDispatcher
    assert type(activemq_worker_manager) == ActivemqWorkerManager
    assert type(mocked_store_image_msg) == StoreImageMsg
    assert type(mocked_store_image_reply_msg) == StoreImageReplyMsg
    assert type(activemq_cache_manager) == ActivemqCacheManager
    
    activemq_worker_manager.submit_threadpool()

    activemq_dispatcher.send_store_image_message(
        msg=mocked_store_image_msg
        )
    
    assert activemq_cache_manager.await_reply_message(
        correlation_id=mocked_store_image_msg.correlation_id
        ) == mocked_store_image_reply_msg
    
    activemq_worker_manager.stop_threadpool()
