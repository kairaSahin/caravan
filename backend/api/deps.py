from dotenv import load_dotenv
from fastapi import Request
from supabase import Client
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.api.auth.jwt_utils import decode_game_player_token, GamePlayerTokenPayload
import os

bearer = HTTPBearer()

load_dotenv()


def get_supabase(request: Request) -> Client:
	return request.app.state.supabase


def get_auth_payload(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> GamePlayerTokenPayload:
	try:
		return decode_game_player_token(
			token=creds.credentials,
			secret_key=os.environ["JWT_SECRET_KEY"],
		)
	# TODO: Maybe catch other exceptions;
	except ValueError:
		raise HTTPException(status_code=401, detail="Invalid token")
	except Exception:
		raise HTTPException(status_code=500, detail="Authentication processing failed")
