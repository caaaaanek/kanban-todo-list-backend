from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserOut
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


def get_session_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    return service.register(email=data.email, password=data.password)


@router.post("/login")
def login(data: UserCreate, request: Request, service: AuthService = Depends(get_auth_service)):
    user = service.login(email=data.email, password=data.password)
    request.session["user_id"] = user.id
    return {"message": "Logged in"}


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}


@router.get("/me", response_model=UserOut)
def me(service: AuthService = Depends(get_auth_service), user_id: int = Depends(get_session_user_id)):
    return service.get_current_user(user_id)
