import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Handle all exceptions here."""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={'error': 'Client Error', 'message': str(http_exception.detail)}
            )
        except ValueError as value_error:
            return JSONResponse(
                status_code=400,
                content={'error': 'Client Error', 'message': str(value_error)}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={'error': 'Internal Server Error', 'message': 'An unexpected error occured'}
            )