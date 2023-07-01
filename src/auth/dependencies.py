'''dependencies.py - Dependency Injection for router.py'''

from http import HTTPStatus
import logging
from fastapi import Depends, HTTPException, Request
from src.auth.schemas import SessionData
from src.auth.utils import decoded_value
import src.config as config
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from starlette.responses import RedirectResponse
from fastapi.security import APIKeyCookie
from urllib.parse import quote_plus, urlencode

class Auth0:
    def __init__(self) -> None:
        self.client: StarletteOAuth2App = self.register_client()
    
    def register_client(self):
        oauth = OAuth()
        oauth.register(
            name='auth0',
            client_id=config.AUTH0_CLIENT_ID,
            client_secret=config.AUTH0_CLIENT_SECRET,
            api_base_url=config.AUTH0_DOMAIN,
            access_token_url=f'https://{config.AUTH0_DOMAIN}/oauth/token',
            authorize_url=f'https://{config.AUTH0_DOMAIN}/authorize',
            client_kwargs={
                'scope': 'openid profile email',
            },
            server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration',
        )
        return oauth.auth0

    async def get_token(self, request) -> dict:
        try:

            return await self.client.authorize_access_token(request)
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized."
            ) from e

    async def authorize_redirect(self, request: Request, redirect_uri: str):
        try:

            return await self.client.authorize_redirect(request, redirect_uri)
        except HTTPException as e:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Not found."
            ) from e
            
    def logout_redirect(self, redirect_uri: str):
        return RedirectResponse(
            url=f"https://{config.AUTH0_DOMAIN}/v2/logout?" 
            + urlencode(
                {
                    "returnTo": redirect_uri,
                    "client_id": config.AUTH0_CLIENT_ID
                },
                quote_via=quote_plus,
            )
        )


api_key_cookie = APIKeyCookie(name=config.APP_COOKIE_NAME, auto_error=True)


def session_data(
    cookie: str = Depends(api_key_cookie)
    ) -> SessionData:
    try:
        return SessionData.parse_obj(decoded_value(cookie))
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Unprocessable entity.",
        ) from e
