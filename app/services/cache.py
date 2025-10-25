import redis.asyncio as redis
from app.core.config import settings

_redis = None

async def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis

async def get_cached_url(short_code: str):
    r = await get_redis()
    return await r.get(short_code)

async def set_cached_url(short_code: str, original_url: str, ttl: int = 3600):
    r = await get_redis()
    await r.set(short_code, original_url, ex=ttl)
