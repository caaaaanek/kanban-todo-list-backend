from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI
from starsessions import SessionAutoloadMiddleware, SessionMiddleware
from starsessions.stores.redis import RedisStore

from app.core.config import settings
from app.routers import auth, boards, columns, tasks

redis_client = aioredis.from_url(settings.REDIS_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()


app = FastAPI(title="Kanban Todo List API", lifespan=lifespan)

store = RedisStore(connection=redis_client)
app.add_middleware(SessionAutoloadMiddleware)
app.add_middleware(
    SessionMiddleware,
    store=store,
    lifetime=settings.SESSION_EXPIRE_SECONDS,
    cookie_https_only=False,
    cookie_same_site="lax",
)

app.include_router(auth.router)
app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(tasks.router)


@app.get("/health")
def health():
    return {"status": "ok"}
