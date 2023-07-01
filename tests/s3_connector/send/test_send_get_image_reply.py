import logging

import pytest
import stomp
import stomp.utils

import src.config as config
from src.s3_connector.message import (DeleteImageMsg, GetImageMsg,
                                      GetImageReplyMsg, StoreImageMsg,
                                      StoreImageReplyMsg)
from src.s3_connector.utils import FilenameGenerator
from tests.test_base import *


@pytest.fixture()
def mocked_url(
    mocked_upload_file_png: UploadFile,
    ) -> str:
    return f'my_mocked_url.com/get/{FilenameGenerator.generate(user_id=1, original_filename=mocked_upload_file_png.filename)}'

@pytest.fixture()
def mocked_store_image_reply_msg(
    mocked_url: str,
    correlation_id: str = '5678'
    ) -> GetImageReplyMsg:
    return GetImageReplyMsg(
        url=mocked_url,
        correlation_id=correlation_id
        )

def test_send(
    send_conn: stomp.Connection11,
    mocked_store_image_reply_msg: GetImageReplyMsg
    ) -> None:
    assert isinstance(send_conn, stomp.Connection11)
    assert isinstance(mocked_store_image_reply_msg, GetImageReplyMsg)
    
    
    send_conn.send(
        destination=config.ACTIVEMQ_STORE_IMAGE_REPLY_QUEUE,
        body=mocked_store_image_reply_msg.serialize(),
        headers={
            'content-type': 'multipart/mixed',
            'correlation_id': mocked_store_image_reply_msg.correlation_id
            }
    )

