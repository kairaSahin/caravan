import logging

from dotenv import load_dotenv
from fastapi import Request
from supabase import Client
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.api.auth.jwt_utils import decode_game_player_token, GamePlayerTokenPayload
from jwt import exceptions as jwt_exceptions
import os

bearer = HTTPBearer()

load_dotenv()
logger = logging.getLogger("caravan.api")


def get_supabase(request: Request) -> Client:
	return request.app.state.supabase


def get_auth_payload(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> GamePlayerTokenPayload:
	try:
		return decode_game_player_token(
			token=creds.credentials,
			secret_key=os.environ["JWT_SECRET_KEY"],
		)
	except jwt_exceptions.ExpiredSignatureError:
		raise HTTPException(status_code=401, detail="Token expired")
	except (ValueError, jwt_exceptions.DecodeError, jwt_exceptions.InvalidTokenError):
		raise HTTPException(status_code=401, detail="Invalid token")
	except Exception:
		logger.exception("Token authentication processing failed")
		raise HTTPException(status_code=500, detail="Authentication processing failed")
