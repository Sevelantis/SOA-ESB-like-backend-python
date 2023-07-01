'''router.py is a core of each module with all the endpoints'''

from http import HTTPStatus
import json

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import src.user.schemas as schemas
from src.database.dependencies import database
import src.user.models as models
from src.user.dependencies import current_user, user_repository
from src.user.repository import UserRepository

user_router = APIRouter()

@user_router.get('/api/v1/user')
async def get_user(
    request: Request, 
    current_user: models.User = Depends(current_user),
    ):
    history = current_user.conv_history
    user_read = schemas.UserRead(
        id=current_user.id,
        email=current_user.email,
        nickname=current_user.nickname,
        auth_type=current_user.auth_type,
        premium=True if current_user.premium==1 else False,
        email_notification=True if current_user.email_notification==1 else False,
        sms_notification=True if current_user.sms_notification==1 else False,
        whatsapp_notification=True if current_user.whatsapp_notification==1 else False,
        profile_picture=current_user.profile_picture,
        conv_history=history.strip('[]').replace("'", "").split(", ")
    )
    return Response(
        content=user_read.json(),
        status_code=HTTPStatus.OK
    )


# @user_router.post('/api/v1/user/history')
# async def add_conv(
#     user_repo: UserRepository = Depends(user_repository),
#     current_user: models.User = Depends(current_user),
# ):
#     import uuid
#     name = f'{uuid.uuid4()}.jpeg'
#     user_repo.update_conv_history(
#         user=current_user,
#         filename=name
#     )

#     return Response(
#         content=f'added {name}',
#         status_code=HTTPStatus.OK
#     )
