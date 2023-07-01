import logging
import time

import pytest
import stomp
import stomp.utils

import src.config as config
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import (ActiveMqConnectionFactory,
                                  ActivemqWorkerFactory, MessageFactory)
from src.activemq.manager import ActivemqWorkerManager
from src.activemq.utils import SubIdGenerator
from src.activemq.worker import ActiveMqWorker
from src.notification.message import NotificationMsg
from src.s3_connector.listener import (GetImageReplyListener,
                                       StoreImageReplyListener)
from src.s3_connector.message import (DeleteImageMsg, GetImageMsg,
                                      GetImageReplyMsg, StoreImageMsg,
                                      StoreImageReplyMsg)
from tests.test_base import *

received_notification_msg = None

@pytest.fixture()
def mocked_notification_worker() -> ActiveMqWorker:
    class MockedNotificationListener(stomp.ConnectionListener):
        def __init__(self) -> None:
            super().__init__()
        def on_message(self, frame: stomp.utils.Frame):
            msg = NotificationMsg()
            msg.deserialize(frame=frame)
            global received_notification_msg
            received_notification_msg = msg
            
    return ActiveMqWorker(
        connection=ActiveMqConnectionFactory.create_connection(
            listener=MockedNotificationListener()
        ),
        sub_id=SubIdGenerator.generate_next(),
        queue=config.ACTIVEMQ_SEND_NOTIFICATION_QUEUE
    )
    
@pytest.fixture()
def activemq_worker_manager(
    mocked_notification_worker: ActiveMqWorker
):
    return ActivemqWorkerManager(workers=[
            mocked_notification_worker
    ])
    
@pytest.fixture()
def mocked_notification_msg(
    message_factory: MessageFactory
    ) -> NotificationMsg:
    return message_factory.create_notification_message(
        email='test@xyz.com',
        subject='sub sub subject',
        message='mes mes message'
    )

def test_send_notification(
    activemq_dispatcher: ActivemqDispatcher, 
    activemq_worker_manager: ActivemqWorkerManager,
    mocked_notification_msg: NotificationMsg
    ):
    assert type(activemq_dispatcher) == ActivemqDispatcher
    assert type(activemq_worker_manager) == ActivemqWorkerManager
    assert type(mocked_notification_msg) == NotificationMsg
    
    activemq_worker_manager.submit_threadpool()

    activemq_dispatcher.send_notification_message(
        msg=mocked_notification_msg
        )
    
    time.sleep(3)
    
    assert received_notification_msg == mocked_notification_msg
    
    activemq_worker_manager.stop_threadpool()
