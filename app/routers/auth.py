from http.client import HTTPException

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starsessions import regenerate_session_id

from app.auth import get_current_user
from app.core.security import verify_password, hash_password
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, request: Request, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=409, detail="Username already taken")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    request.session["user_id"] = user.id  # ← додати
    request.session["role"] = user.role.value  # ← додати
    return user


@router.post("/login", response_model=UserResponse)
async def login(data: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    regenerate_session_id(request)  # ← прибрати await
    request.session["user_id"] = user.id
    request.session["role"] = user.role.value
    return user


@router.post("/logout", status_code=204)
async def logout(request: Request):
    request.session.clear()


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)):
    return user
