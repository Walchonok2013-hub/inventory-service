from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt as jose_jwt, JWTError  # 1. Переименовываем библиотеку в jose_jwt, чтобы не путать с функцией
from app.core.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    # 2. Используем переименованную библиотеку jose_jwt
    encoded_jwt = jose_jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        # 3. Используем переименованную библиотеку jose_jwt
        payload = jose_jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None