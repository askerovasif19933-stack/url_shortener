from redis.asyncio import Redis

redis = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


async def get_from_cache(slug: str) -> str | None:
    """Получает длинный URL из кеша по короткому slug."""
    return await redis.get(slug)


async def set_to_cache(slug: str, long_url: str, ttl: int = 3600):
    """Сохраняет длинный URL в кеш с коротким slug и временем жизни ttl."""
    await redis.set(slug, long_url, ex=ttl)


#pip install redis 
#docker run -d -p 6379:6379 --name redis redis
