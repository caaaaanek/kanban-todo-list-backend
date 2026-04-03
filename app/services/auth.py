from fastapi import HTTPException

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, username: str, email: str, password: str) -> User:
        if self.repo.get_by_username(username):
            raise HTTPException(status_code=409, detail="Username already taken")
        if self.repo.get_by_email(email):
            raise HTTPException(status_code=409, detail="Email already registered")
        return self.repo.create(
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )

    def login(self, username: str, password: str) -> User:
        user = self.repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    def get_by_id(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return user
