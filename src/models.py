
from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column





class ShortURL(Base):
    """Модель для хранения коротких URL."""
    __tablename__ = 'short_urls'

    slug: Mapped[str] = mapped_column(primary_key=True)
    long_url: Mapped[str]