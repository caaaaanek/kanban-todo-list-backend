from fastapi import HTTPException

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, email: str, password: str) -> User:
        if self.repo.get_by_email(email):
            raise HTTPException(status_code=400, detail="Email already registered")
        return self.repo.create(email=email, hashed_password=hash_password(password))

    def login(self, email: str, password: str) -> User:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    def get_current_user(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
