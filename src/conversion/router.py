'''router.py is a core of each module with all the endpoints'''

import logging
from http import HTTPStatus

from fastapi import (APIRouter, Depends, FastAPI, File, Form, HTTPException,
                     Request, Response, UploadFile)

import src.config as config
import src.user.models as models
from src.activemq.cache.manager import ActivemqCacheManager
from src.activemq.cache.utils import CorrelationIdGenerator
from src.activemq.dependencies import (activemq_cache_manager,
                                       activemq_dispatcher)
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import MessageFactory
from src.conversion.message import ConvertImageReplyMsg
from src.conversion.schemas import ConversionCreate, ConversionRead
from src.s3_connector.message import StoreImageReplyMsg
from src.s3_connector.utils import FilenameGenerator
from src.user.dependencies import current_user, user_repository
from src.user.repository import UserRepository

conversion_router = APIRouter()

@conversion_router.post('/api/v1/convert')
async def convert_to_jpeg(
    conv_create: ConversionCreate = Depends(ConversionCreate),
    image: UploadFile = File(),
    dispatcher: ActivemqDispatcher = Depends(activemq_dispatcher),
    message_factory: MessageFactory = Depends(MessageFactory),
    activemq_cache_manager: ActivemqCacheManager = Depends(activemq_cache_manager),
    current_user: models.User = Depends(current_user),
    user_repo: UserRepository = Depends(user_repository),
    ):
    correlation_id = CorrelationIdGenerator.generate()
    # correlation_id = '1234' # integration local test
    dispatcher.send_convert_image_message(
        message_factory.create_convert_image_message(
            file=image, 
            conv_create=conv_create, 
            correlation_id=correlation_id
            )
        )
    convert_reply = None
    try: 
        convert_reply: ConvertImageReplyMsg = await activemq_cache_manager.await_reply_message(
            correlation_id=correlation_id
        )
    except HTTPException as e:
        if e.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            return Response(
                content='Waiting for conversion message too long',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
                )
    logging.info(f'Received converted image: {convert_reply}. Sending store message...')
    

    correlation_id = CorrelationIdGenerator.generate()
    # correlation_id = '5678' # integration local test
    dispatcher.send_store_image_message(
        message_factory.create_store_image_message(
            filename=FilenameGenerator.generate(
                user_id=current_user.id,
                ext=conv_create.target_format),
            image_data=convert_reply.image_data,
            correlation_id=correlation_id            
        )
    )
    try:
        store_reply: StoreImageReplyMsg = await activemq_cache_manager.await_reply_message(
            correlation_id=correlation_id
        )
    except HTTPException as e:
        if e.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            return Response(
                content='Waiting for conversion message too long',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
                )
    user_repo.update_conv_history(
        user=current_user,
        filename=store_reply.url
    )

    logging.info(f'Received store image, link: {store_reply.url}. Sending notification..')
    
    
    
    dispatcher.send_notification_message(
        message_factory.create_notification_message(
            email=current_user.email,
            subject='Your conversion download link!',
            message=f'Thank you for using our product. Your link is here: {store_reply.url}'
        )
    )
    logging.info(f'Notification sent. Sending response...')

    return Response(
        status_code=HTTPStatus.OK,
        content=ConversionRead(
            target_format=conv_create.target_format,
            link = store_reply.url
        ).json()
        )
