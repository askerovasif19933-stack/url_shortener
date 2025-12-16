from starlette import status as STATUS
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from src.db import engine, Base
from service import create_short_url, get_url_by_slug
from src.crud import cash_long_url
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация базы данных при старте приложения."""
    # Startup code here
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown code here


app = FastAPI(lifespan=lifespan)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/", response_class=HTMLResponse)
async def index():
    """Возвращает главную страницу приложения."""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()




@app.post("/short_url")
async def generate_short_url(long_url: str=Body(embed=True)):
    """Генерирует короткий URL для данного long_url."""
    slug = await create_short_url(long_url)

    return {'slug': slug}



@app.get("/{slug}")
async def redirect_to_long_url(slug: str):
    """Перенаправляет на длинный URL по короткому slug."""
    long_url = await get_url_by_slug(slug)
    if not long_url:
        raise HTTPException(status_code=STATUS.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=long_url, status_code=STATUS.HTTP_302_FOUND)
    



# uvicorn main:app --reload
