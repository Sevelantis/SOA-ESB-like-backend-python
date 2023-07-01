

import datetime
from email.utils import format_datetime
from http import HTTPStatus
import logging
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from src.auth.schemas import SessionData
from src.auth.utils import encoded_value
import src.user.models as models

import src.config as config

class ResponseFactory:
    def __init__(self) -> None:
        pass


    def auth_response(self, user: models.User) -> Response:
        response = RedirectResponse(url=f'http://{config.CORS_ORIGIN_DNS}/')
        expiry = datetime.datetime.utcnow()
        expiry += datetime.timedelta(days=999)
        expires = expiry.strftime('%a, %d-%b-%Y %T GMT')
        response.set_cookie(
            key = config.APP_COOKIE_NAME,
            value = encoded_value(SessionFactory.create_session(user=user)),
            domain = config.WEB_SERVICE_AUDIENCE,
            path = '/',
            samesite="lax",    
            secure=False,
            expires=expires,
            max_age='123123123',
            httponly=False
            )
        
        logging.info(
            f'''Sending set-cookie response... Response:
            code: {response.status_code}
            body: {response.body}
            cookie: {response.headers.get('set-cookie')}
            ''')
        return response
    
    
    def logout_response(self, response: Response) -> Response:
        response.delete_cookie(
            key = config.APP_COOKIE_NAME,
            domain = config.WEB_SERVICE_AUDIENCE,
            path = '/',
            samesite = "lax",
            secure=False,
            httponly=False,
            )
        
        return response

class SessionFactory:

    @classmethod
    def create_session(cls, user: models.User) -> dict:
        return SessionData(
            user_id=user.id,
            user_identification=user.email or user.nickname,
            auth_type=user.auth_type,
        ).__dict__
