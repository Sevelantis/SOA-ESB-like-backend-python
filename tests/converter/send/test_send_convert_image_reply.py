
import logging
import time

import pytest
import stomp
import stomp.utils

import src.config as config
from src.activemq.cache.utils import CorrelationIdGenerator
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import (ActiveMqConnectionFactory,
                                  ActivemqWorkerFactory, MessageFactory)
from src.activemq.manager import ActivemqWorkerManager
from src.activemq.utils import SubIdGenerator
from src.activemq.worker import ActiveMqWorker
from src.s3_connector.listener import (GetImageReplyListener,
                                       StoreImageReplyListener)
from src.s3_connector.message import (DeleteImageMsg, GetImageMsg,
                                      GetImageReplyMsg, StoreImageMsg,
                                      StoreImageReplyMsg)
from tests.test_base import *


@pytest.fixture()
def mocked_convert_image_reply_msg(
    mocked_upload_file_png: UploadFile,
    correlation_id: str = '1234'
    ) -> ConvertImageReplyMsg:
    return ConvertImageReplyMsg(
        image_data=mocked_upload_file_png.file.read(),
        correlation_id=correlation_id
        )

def test_send(
    send_conn: stomp.Connection11,
    mocked_convert_image_reply_msg: ConvertImageReplyMsg
    ) -> None:
    assert isinstance(send_conn, stomp.Connection11)
    assert isinstance(mocked_convert_image_reply_msg, ConvertImageReplyMsg)

    send_conn.send(
        destination=config.ACTIVEMQ_CONVERT_IMAGE_REPLY_QUEUE,
        body=mocked_convert_image_reply_msg.serialize(),
        headers={
            'content-type': 'multipart/mixed',
            'correlation_id': mocked_convert_image_reply_msg.correlation_id
            }
    )

