import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

logger = logging.getLogger('uvicorn')
logger.setLevel(logging.DEBUG)

class RequestProcessMiddleware(BaseHTTPMiddleware):
    """Handle all exceptions here."""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response =  await call_next(request)
        process_time = (time.time() - start_time)
        formatted_process_time = '{0:.4f}'.format(process_time)
        logger.info(f'{request.method} {request.url} {formatted_process_time}s')
        response.headers['X-Process-Time'] = formatted_process_time
        return response
