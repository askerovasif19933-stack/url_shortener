from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL, ALEMBIC_DATABASE_URL, REDIS_URL

DATABASE_URL = DATABASE_URL
ALEMBIC_DATABASE_URL = ALEMBIC_DATABASE_URL
REDIS_URL = REDIS_URL

class Base(DeclarativeBase):
    pass

engine = create_async_engine(url=f'{DATABASE_URL}')


get_session = async_sessionmaker(bind=engine, expire_on_commit=False)