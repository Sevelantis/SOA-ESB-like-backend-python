import io
from fastapi import UploadFile
import pytest
import stomp
from src.activemq.cache.manager import ActivemqCacheManager
from src.activemq.cache.cache import ActivemqMessageCache
from src.conversion.schemas import ConversionCreate
from src.conversion.message import ConvertImageMsg, ConvertImageReplyMsg
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import ActiveMqConnectionFactory, MessageFactory
from src.conversion.listener import ConvertImageReplyListener
import src.config as config
import logging


@pytest.fixture()
def send_conn() -> stomp.connect.StompConnection11:
    return ActiveMqConnectionFactory.create_connection()

@pytest.fixture()
def activemq_dispatcher(send_conn: stomp.connect.StompConnection11):
    return ActivemqDispatcher(conn=send_conn)

@pytest.fixture()
def message_factory() -> MessageFactory:
    return MessageFactory()

@pytest.fixture()
def mocked_upload_file_jpg(ext = 'jpg') -> UploadFile:
    with open(f'sample_images/raccoon.{ext}', 'rb') as f:
        return UploadFile(
            filename=f'raccoon.{ext}',
            file=io.BytesIO(f.read()),
            headers={"content-type": "image/jpeg"}
            )

@pytest.fixture()
def mocked_upload_file_png(ext = 'png') -> UploadFile:
    with open(f'sample_images/raccoon.{ext}', 'rb') as f:
        return UploadFile(
            filename=f'raccoon.{ext}',
            file=io.BytesIO(f.read()),
            headers={"content-type": "image/png"}
            )

@pytest.fixture()
def activemq_message_cache():
    return ActivemqMessageCache()

@pytest.fixture()
def activemq_cache_manager(
    activemq_message_cache: ActivemqMessageCache
):
    return ActivemqCacheManager(
        activemq_message_cache=activemq_message_cache
    )
