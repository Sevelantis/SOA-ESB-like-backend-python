import logging
import time

import pytest
import stomp
import stomp.utils
from fastapi import UploadFile

import src.config as config
from src.activemq.cache.utils import CorrelationIdGenerator
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import (ActiveMqConnectionFactory,
                                  ActivemqWorkerFactory, MessageFactory)
from src.activemq.manager import ActivemqWorkerManager
from src.activemq.utils import SubIdGenerator
from src.activemq.worker import ActiveMqWorker
from src.conversion.message import ConvertImageMsg, ConvertImageReplyMsg
from src.conversion.schemas import ConversionCreate
from tests.test_base import *


@pytest.fixture()
def mocked_convert_image_worker(
    send_conn: stomp.connect.StompConnection11,
    mocked_convert_image_reply_msg: ConvertImageReplyMsg
    ) -> ActiveMqWorker:
    class MockedConvertImageListener(stomp.ConnectionListener):
        def __init__(self) -> None:
            super().__init__()
        def on_message(self, frame: stomp.utils.Frame):
            msg = ConvertImageMsg()
            msg.deserialize(frame=frame)
            # for debug
            # with open('sample_images/result.jpg', 'wb') as f:
            #     f.write(msg.image_data)
            # send back mocked message
            send_conn.send(
                destination=config.ACTIVEMQ_CONVERT_IMAGE_REPLY_QUEUE,
                body=mocked_convert_image_reply_msg.serialize(),
                headers={
                    'content-type': 'multipart/mixed',
                    'correlation_id': mocked_convert_image_reply_msg.correlation_id
                    }
            )
            
    return ActiveMqWorker(
        connection=ActiveMqConnectionFactory.create_connection(
            listener=MockedConvertImageListener()
        ),
        sub_id=SubIdGenerator.generate_next(),
        queue=config.ACTIVEMQ_CONVERT_IMAGE_QUEUE
    )

@pytest.fixture()
def convert_image_reply_worker() -> ActiveMqWorker:
    return ActivemqWorkerFactory.create_convert_image_reply_worker()

@pytest.fixture()
def activemq_worker_manager(
    mocked_convert_image_worker: ActiveMqWorker,
    convert_image_reply_worker: ActiveMqWorker
):
    return ActivemqWorkerManager(workers=[
            mocked_convert_image_worker,
            convert_image_reply_worker
    ])

@pytest.fixture()
def correlation_id() -> str:
    return CorrelationIdGenerator.generate()

@pytest.fixture()
def mocked_convert_image_msg(
    message_factory: MessageFactory,
    mocked_upload_file_jpg: UploadFile,
    correlation_id: str
    ) -> ConvertImageMsg:
    return message_factory.create_convert_image_message(
        file=mocked_upload_file_jpg,
        conv_create=ConversionCreate(format='png', size=9876),
        correlation_id=correlation_id
    )
    
@pytest.fixture()
def mocked_convert_image_reply_msg(
    mocked_upload_file_png: UploadFile,
    correlation_id: str
    ) -> ConvertImageReplyMsg:
    return ConvertImageReplyMsg(
        image_data=mocked_upload_file_png.file.read(),
        correlation_id=correlation_id
        )

def test_convert_image(
    activemq_dispatcher: ActivemqDispatcher, 
    activemq_worker_manager: ActivemqWorkerManager,
    mocked_convert_image_msg: ConvertImageMsg,
    mocked_convert_image_reply_msg: ConvertImageReplyMsg,
    activemq_cache_manager: ActivemqCacheManager
    ):
    assert type(activemq_dispatcher) == ActivemqDispatcher
    assert type(activemq_worker_manager) == ActivemqWorkerManager
    assert type(mocked_convert_image_msg) == ConvertImageMsg
    assert type(mocked_convert_image_reply_msg) == ConvertImageReplyMsg
    assert type(activemq_cache_manager) == ActivemqCacheManager
    
    activemq_worker_manager.submit_threadpool()

    activemq_dispatcher.send_convert_image_message(
        msg=mocked_convert_image_msg
        )
    
    assert activemq_cache_manager.await_reply_message(
        correlation_id=mocked_convert_image_msg.correlation_id
        ) == mocked_convert_image_reply_msg
    
    activemq_worker_manager.stop_threadpool()
