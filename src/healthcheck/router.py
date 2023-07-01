from http import HTTPStatus
from fastapi import APIRouter
from starlette.responses import JSONResponse

healthcheck_router = APIRouter()

@healthcheck_router.get('/api/v1/healthcheck')
async def homepage():
    return JSONResponse(content='I am ok.', status_code=HTTPStatus.OK)
