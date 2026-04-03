from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.routers import auth, boards, columns, tasks

app = FastAPI(title="Kanban Todo List API")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY, max_age=settings.SESSION_EXPIRE_SECONDS)

app.include_router(auth.router)
app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(tasks.router)


@app.get("/health")
def health():
    return {"status": "ok"}
