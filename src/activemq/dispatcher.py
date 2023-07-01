import logging
import stomp.connect as connect
from src.notification.message import NotificationMsg
from src.s3_connector.message import DeleteImageMsg, StoreImageMsg, GetImageMsg
from src.conversion.message import ConvertImageMsg

import src.config as config

class ActivemqDispatcher:
    def __init__(self, conn: connect.StompConnection11) -> None:
        self.conn = conn
        
    def send_convert_image_message(self, msg: ConvertImageMsg) -> None:
        logging.info(msg)
        self.conn.send(
            destination=config.ACTIVEMQ_CONVERT_IMAGE_QUEUE,
            body=msg.serialize(),
            headers={
                'content-type': 'multipart/mixed',
                'correlation_id': msg.correlation_id
            }
        )
        
    def send_store_image_message(self, msg: StoreImageMsg) -> None:
        logging.info(msg)
        self.conn.send(
            destination=config.ACTIVEMQ_STORE_IMAGE_QUEUE,
            body=msg.serialize(),
            headers={
                'content-type': 'multipart/mixed',
                'correlation_id': msg.correlation_id
            }
        )
        
    def send_get_image_message(self, msg: GetImageMsg) -> None:
        logging.info(msg)
        self.conn.send(
            destination=config.ACTIVEMQ_GET_IMAGE_QUEUE,
            body=msg.serialize(),
            headers={
                'content-type': 'multipart/mixed',
                'correlation_id': msg.correlation_id
            }
        )
        
    def send_delete_image_message(self, msg: DeleteImageMsg) -> None:
        logging.info(msg)
        self.conn.send(
            destination=config.ACTIVEMQ_DELETE_IMAGE_QUEUE,
            body=msg.serialize(),
            headers={
                'content-type': 'multipart/mixed'
            }
        )
        
    def send_notification_message(self, msg: NotificationMsg) -> None:
        logging.info(msg)
        self.conn.send(
            destination=config.ACTIVEMQ_SEND_NOTIFICATION_QUEUE,
            body=msg.serialize(),
            headers={
                'content-type': 'multipart/mixed'
            }
        )
