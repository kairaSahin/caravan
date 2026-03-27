from contextlib import asynccontextmanager
from logging import Logger

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from supabase import create_client, Client
import os

from backend.api.logger.exception_handlers import http_exception_handler_func, unhandled_exception_handler_func
from backend.api.logger.logging import configure_error_logging
from backend.api.routes import moves, state
from starlette.exceptions import HTTPException as StarletteHTTPException

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
	# TODO: Add error handling on env variables, may change connection with RLS policies;
	app.state.supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SECRET_KEY"])
	yield


app = FastAPI(lifespan=lifespan)
app.include_router(moves.router)
app.include_router(state.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
	return await http_exception_handler_func(logger, request, exc)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
	return await unhandled_exception_handler_func(logger, request, exc)


logger = configure_error_logging()
