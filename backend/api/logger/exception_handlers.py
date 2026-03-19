from logging import Logger

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi import Request


async def http_exception_handler_func(logger: Logger, request: Request, exc: StarletteHTTPException) -> JSONResponse:
	if exc.status_code >= 500:
		logger.error(f"HTTP {exc.status_code} at {request.method} {request.url.path}: {exc.detail}")

	return JSONResponse(
		status_code=exc.status_code,
		content={"detail": exc.detail},
		headers=exc.headers,
	)


async def unhandled_exception_handler_func(logger: Logger, request: Request, exc: Exception) -> JSONResponse:
	logger.exception(f"Unhandled exception at {request.method} {request.url.path}: {exc}")
	return JSONResponse(status_code=500, content={"detail": "Internal server error"})
