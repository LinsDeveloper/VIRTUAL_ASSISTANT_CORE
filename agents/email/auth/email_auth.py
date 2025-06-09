import os
import time
from typing import Dict, Optional, Union
import requests
from dotenv import load_dotenv
import redis
from helpers.cache.cache_store import token_cache
import jwt

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True
)

def authenticate_gmail() -> str:
    accessToken = token_cache["accessToken"]
    claims = jwt.decode(accessToken, options={"verify_signature": False})
    user_id = claims.get("nameid")
    gmail_token = redis_client.get(f"GMAIL-{user_id}")
    return gmail_token