from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from jose import jwt
from datetime import datetime, timedelta
from .config import settings

pwd_context = PasswordHasher()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(hashed_password, password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False


def create_token(data: dict, expires_minutes: int = 60) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")