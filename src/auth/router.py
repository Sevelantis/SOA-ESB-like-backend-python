'''router.py is a core of each module with all the endpoints'''

import json
import logging
from http import HTTPStatus

from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     routing)
from starlette.responses import JSONResponse, RedirectResponse

import src.user.models as models
from src.activemq.dependencies import activemq_dispatcher
from src.activemq.dispatcher import ActivemqDispatcher
from src.activemq.factory import MessageFactory
from src.auth.dependencies import Auth0, api_key_cookie
from src.auth.factory import ResponseFactory
from src.auth.utils import decoded_value
from src.user.dependencies import user_manager
from src.user.manager import UserManager

auth_router = APIRouter()

@auth_router.get('/api/v1/auth')
async def auth(
    request: Request, 
    auth_client: Auth0 = Depends(Auth0), 
    user_manager: UserManager = Depends(user_manager),
    response_factory: ResponseFactory = Depends(ResponseFactory),
    dispatcher: ActivemqDispatcher = Depends(activemq_dispatcher),
    message_factory: MessageFactory = Depends(MessageFactory),
    ):
    logging.info(
        f'''Obtaining token... Request:
        cookie: {request.cookies.keys()}
        base_url: {request.base_url}
        url: {request.url}
        ''')
    token: dict = await auth_client.get_token(request)
    logging.info(
        f'''Is token present: {token is not None}... Request:
        cookie: {request.cookies.keys()}
        base_url: {request.base_url}
        url: {request.url}
        ''')
    logging.info(f'Processing user auth... userinfo: {token["userinfo"]}')
    user: models.User = user_manager.process_user_auth(userinfo=token['userinfo'])
    logging.info(f'User email: {user.email} ')
    
    if user:
        dispatcher.send_notification_message(
            message_factory.create_notification_message(
                email=user.email,
                subject='New Login Activity',
                message=f'''
                Logged in to http://egs-conv.deti using your email.
                Start converting here: http://egs-conv.deti/convert
                
                Regards,
                Your ImgConv team
                '''
            )
        )

    return response_factory.auth_response(user=user)


@auth_router.get('/api/v1/login')
async def login(
    request: Request, 
    auth_client: Auth0 = Depends(Auth0)
    ):
    redirect_uri = request.url_for('auth')
    logging.info(f'login: redirect uri: {redirect_uri}, adding Access-Control-Allow-Origin')

    return await auth_client.authorize_redirect(request, redirect_uri)


@auth_router.get("/api/v1/logout")
async def logout(
    request: Request,
    auth_client: Auth0 = Depends(Auth0), 
    cookie: str = Depends(api_key_cookie),
    response_factory: ResponseFactory = Depends(ResponseFactory)
    ):
    
    return response_factory.logout_response(
        response=auth_client.logout_redirect(redirect_uri=request.url_for('homepage'))
        )   


@auth_router.get('/')
async def homepage(cookie: str = Depends(api_key_cookie)):

    return JSONResponse(content=f'Decoded cookie: {decoded_value(cookie)}', status_code=HTTPStatus.OK)
