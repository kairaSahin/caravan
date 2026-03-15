from fastapi import Request
from supabase import Client


def get_supabase(request: Request) -> Client:
	return request.app.state.supabase
