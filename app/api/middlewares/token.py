from datetime import datetime, timedelta

import bcrypt
import jwt

from app.core.settings import settings
from app.utils.errors.error import CustomErrorCode, error_service


# token
def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.acces_token_expiration_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()

    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    to_encode.update({"iat": now})

    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    except jwt.InvalidTokenError as e:
        raise error_service.error(CustomErrorCode.HTTP_401_UNAUTHORIZED)
    return decoded


def create_token(token_type: str, payload: dict):
    token_payload = payload.copy()
    token_payload["token_type"] = token_type
    return token_payload


# password
def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode(), salt)
    return hash_password


def validate_password(password: str, hash_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password)
