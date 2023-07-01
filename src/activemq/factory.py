from fastapi import UploadFile
import stomp
import stomp.connect as connect
from src.activemq.cache.cache import ActivemqMessageCache
from src.s3_connector.listener import GetImageReplyListener, StoreImageReplyListener
from src.activemq.utils import SubIdGenerator
from src.activemq.worker import ActiveMqWorker
from src.conversion.listener import ConvertImageReplyListener
from src.conversion.message import ConvertImageMsg
from src.s3_connector.message import GetImageMsg, StoreImageMsg, DeleteImageMsg
from src.notification.message import NotificationMsg
from src.conversion.schemas import ConversionCreate
import src.config as config

class ActiveMqConnectionFactory:
    
    @classmethod
    def create_connection(
        cls, 
        broker_host: str = config.ACTIVEMQ_HOST, 
        broker_port: int = int(config.ACTIVEMQ_PORT), 
        broker_username: str = config.ACTIVEMQ_USERNAME, 
        broker_password: str = config.ACTIVEMQ_PASSWORD, 
        listener: connect.ConnectionListener=None,
        ssl_active: bool=False
        ) -> connect.StompConnection11:
        conn = stomp.Connection(host_and_ports=[(broker_host, broker_port)])
        if listener:
            conn.set_listener(
                name='', 
                listener=listener
                )
        conn.connect(
            broker_username, 
            broker_password, 
            wait=True
        )
        
        return conn

class ActivemqWorkerFactory:

    @classmethod
    def create_convert_image_reply_worker(cls) -> ActiveMqWorker:
        return ActiveMqWorker(
            connection=ActiveMqConnectionFactory.create_connection(
                listener=ConvertImageReplyListener()
                ),
            sub_id=SubIdGenerator.generate_next(),
            queue=config.ACTIVEMQ_CONVERT_IMAGE_REPLY_QUEUE
        )

    @classmethod
    def create_store_image_reply_worker(cls) -> ActiveMqWorker:
        return ActiveMqWorker(
            connection=ActiveMqConnectionFactory.create_connection(
                listener=StoreImageReplyListener()
                ),
            sub_id=SubIdGenerator.generate_next(),
            queue=config.ACTIVEMQ_STORE_IMAGE_REPLY_QUEUE
        )

    @classmethod
    def create_get_image_reply_worker(cls) -> ActiveMqWorker:
        return ActiveMqWorker(
            connection=ActiveMqConnectionFactory.create_connection(
                listener=GetImageReplyListener()
                ),
            sub_id=SubIdGenerator.generate_next(),
            queue=config.ACTIVEMQ_GET_IMAGE_REPLY_QUEUE
        )

class MessageFactory:
    def __init__(self) -> None:
        pass
    
    def create_convert_image_message(
        self, 
        file: UploadFile, 
        conv_create: ConversionCreate,
        correlation_id: str
        ) -> ConvertImageMsg:
        return ConvertImageMsg(
            image_data=file.file.read(), 
            image_format=conv_create.target_format,
            correlation_id=correlation_id
            )
    
    def create_store_image_message(
        self,
        filename: str,
        image_data: bytes,
        correlation_id: str
        ) -> StoreImageMsg:
        return StoreImageMsg(
            filename=filename,
            image_data=image_data,
            correlation_id=correlation_id
        )
    
    def create_get_image_message(
        self,
        filename: str,
        correlation_id: str
        ) -> GetImageMsg:
        return GetImageMsg(
            filename=filename,
            correlation_id=correlation_id
        )
    
    def create_delete_image_message(
        self,
        filename: str
        ) -> DeleteImageMsg:
        return DeleteImageMsg(
            filename=filename
        )
        
    def create_notification_message(
        self,
        send_email: bool = True,
        send_whatsapp: bool = False,
        send_sms: bool = False,
        email: str = None,
        subject: str = None,
        message: str = None,
        phone_number: str = None,
        ) -> NotificationMsg:
        return NotificationMsg(
            send_email=send_email,
            send_whatsapp=send_whatsapp,
            send_sms=send_sms,
            email=email,
            subject=subject,
            message=message,
            phone_number=phone_number
        )
