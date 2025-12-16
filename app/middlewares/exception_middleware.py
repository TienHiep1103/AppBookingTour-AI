import traceback
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("uvicorn.error")

class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except Exception as e:
            # Log đầy đủ stack trace
            logger.error(
                f"Unhandled exception at {request.url}\n{traceback.format_exc()}"
            )

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal Server Error",
                },
            )
