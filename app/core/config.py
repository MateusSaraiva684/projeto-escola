import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8


settings = Settings()

if not settings.SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY não definida!\n"
        "No Render: vá em Environment e adicione a variável SECRET_KEY.\n"
        "Gere uma chave com: python -c \"import secrets; print(secrets.token_hex(32))\""
    )
