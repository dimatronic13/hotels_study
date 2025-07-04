from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from src.config import settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self):
        self.encoded_jwt = None

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        self.encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return self.encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, token: str):
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],)
        except jwt.exceptions.DecodeError:
            raise HTTPException(detail="Invalid token", status_code=401)
