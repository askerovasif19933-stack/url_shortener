import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from main import app

@pytest.mark.asyncio
@patch("main.create_short_url", new_callable=AsyncMock)
async def test_generate_short_url(mock_create):
    """Тестирует генерацию короткого URL."""
    mock_create.return_value = "abc123"

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/short_url",
            json={"long_url": "https://example.com"}
        )

    assert response.status_code == 200
    assert response.json() == {"slug": "abc123"}



@pytest.mark.asyncio
@patch("main.get_url_by_slug", new_callable=AsyncMock)
async def test_redirect(mock_get):
    """Тестирует перенаправление по короткому URL."""
    mock_get.return_value = "https://example.com"

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/abc123", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com"

