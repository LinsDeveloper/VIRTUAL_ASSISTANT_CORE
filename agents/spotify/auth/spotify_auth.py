import os
import time
from typing import Dict, Optional
import requests
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

_token_cache = TTLCache(maxsize=2, ttl=3600)

def _cache_token(tokens: Dict[str, any]):
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in", 0)
   
    if access_token:
        _token_cache["access_token"] = (access_token, time.time() + expires_in - 10)
        _token_cache.ttl = expires_in
    if refresh_token:
        _token_cache["refresh_token"] = refresh_token

def _get_cached_token() -> Optional[Dict[str, str]]:
    token_tuple = _token_cache.get("access_token")
    refresh_token = _token_cache.get("refresh_token")
    if token_tuple:
        access_token, expires_at = token_tuple
        if time.time() < expires_at:
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": int(expires_at - time.time()),
            }
    return None

def _refresh_token(client_id, client_secret, refresh_token, redirect_uri, token_url):
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        if not tokens.get("refresh_token"):
            tokens["refresh_token"] = refresh_token
        _cache_token(tokens)
        return {
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "expires_in": tokens.get("expires_in"),
        }
    else:
        return None

def authenticate_spotify(mocked: bool = False) -> str:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    token_url = "https://accounts.spotify.com/api/token"

    
    cached = _get_cached_token()
    if cached:
        return cached

   
    refresh_token = _token_cache.get("refresh_token")
    if refresh_token:
        refreshed = _refresh_token(client_id, client_secret, refresh_token, redirect_uri, token_url)
        if refreshed:
            return refreshed

    
    if mocked:
        code = os.getenv("SPOTIFY_AUTH_CODE")
    else:
        raise NotImplementedError("OAuth2 flow não implementado para produção.")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        _cache_token(tokens)
        return tokens.get("access_token")
    else:
        raise Exception(f"Erro ao autenticar com Spotify: {response.text}")