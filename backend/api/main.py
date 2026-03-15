from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client
import os

from backend.api.routes import moves, state

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
	# TODO: Add error handling on env variables, may change connection with RLS policies;
	app.state.supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
	yield


app = FastAPI(lifespan=lifespan)
app.include_router(moves.router)
app.include_router(state.router)
