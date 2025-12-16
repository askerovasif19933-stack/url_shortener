import select
from creat_slug import generate_slug
from src.crud import add_short_url, cash_long_url, get_long_url  
from starlette import status 

async def create_short_url(long_url: str) -> str:
    """
    Создает короткий URL (slug) для данного long_url. Если long_url уже существует, возвращает существующий slug.
    1. Проверяет кеш на наличие long_url.
    2. Если нет, генерирует новый slug и сохраняет его в БД и кеш.
    3. Возвращает slug.
    """
    cash = await cash_long_url(long_url)
    if cash:
        return cash
    slug = generate_slug()
    await add_short_url(slug, long_url)
    return slug




async def get_url_by_slug(slug: str) -> str | None:
    """
    Получает длинный URL по его короткому slug.
    1. Проверяет кеш на наличие slug.
    2. Если нет, ищет в БД.
    3. Возвращает найденный URL или None.
    """
    long_url = await get_long_url(slug)
    return long_url if long_url else None





    

