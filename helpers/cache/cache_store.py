# cache_store.py
from cachetools import TTLCache

token_cache = TTLCache(maxsize=1000, ttl=6000)
