from sqlalchemy import select
from src.db import get_session
from src.models import ShortURL
from src.cache import get_from_cache, set_to_cache



async def add_short_url(slug: str, long_url: str):
    """Добавляет новую запись короткого URL в БД и кеш."""
    async with get_session() as session:
        short_url = ShortURL(slug=slug, long_url=long_url)
        session.add(short_url)
        await session.commit()

    # сразу кладем в кеш
    await set_to_cache(slug, long_url)



async def get_long_url(slug: str) -> str | None:
    """Получает длинный URL по короткому slug, сначала из кеша, потом из БД."""
    # 1️⃣ Пробуем Redis
    cached = await get_from_cache(slug)
    if cached:
        return cached

    # 2️⃣ Если нет — идем в БД
    async with get_session() as session:
        stmt = select(ShortURL).where(ShortURL.slug == slug)
        res = await session.execute(stmt)
        result = res.scalar_one_or_none()

        if not result:
            return None

        # 3️⃣ Кладем в Redis
        await set_to_cache(slug, result.long_url)

        return result.long_url

    


async def cash_long_url(long_url: str) -> None | str:
    """Проверяет в БД наличие long_url и возвращает соответствующий slug, если найден."""

    async with get_session() as session:
        short_url = select(ShortURL.slug).where(ShortURL.long_url == long_url)
        res = await session.execute(short_url)
        result = res.scalars().first()
        return result if result else None