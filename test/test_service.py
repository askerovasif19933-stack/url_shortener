import pytest
from unittest.mock import AsyncMock, patch
from service import create_short_url, get_url_by_slug


@pytest.mark.asyncio
@patch("service.cash_long_url", new_callable=AsyncMock)
@patch("service.add_short_url", new_callable=AsyncMock)
async def test_create_short_url_new(mock_add, mock_cache):
    """Тестирует создание нового короткого URL, когда long_url отсутствует в БД."""
    # если в БД нет такого long_url
    mock_cache.return_value = None

    slug = await create_short_url("https://example.com")

    assert slug is not None
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
@patch("service.get_long_url", new_callable=AsyncMock)
async def test_get_url_by_slug_found(mock_get):
    """Тестирует получение длинного URL по существующему slug."""
    mock_get.return_value = "https://example.com"

    result = await get_url_by_slug("abc123")

    assert result == "https://example.com"