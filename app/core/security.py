from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash: str) -> bool:
    return pwd_context.verify(senha, hash)


def criar_token(data: dict) -> str:
    to_encode = data.copy()
    agora = datetime.now(timezone.utc)
    expire = agora + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire, "iat": agora})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
