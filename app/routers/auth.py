from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starsessions import regenerate_session_id

from app.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    return service.register(data.username, data.email, data.password)


@router.post("/login", response_model=UserResponse)
async def login(
    data: UserLogin,
    request: Request,
    service: AuthService = Depends(get_auth_service),
):
    user = service.login(data.username, data.password)
    await regenerate_session_id(request)
    request.session["user_id"] = user.id
    request.session["role"] = user.role.value
    return user


@router.post("/logout", status_code=204)
async def logout(request: Request):
    request.session.clear()


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)):
    return user
