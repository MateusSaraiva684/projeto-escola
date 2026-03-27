import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./escola.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8

    def __post_init__(self):
        if not self.SECRET_KEY:
            logger.warning(
                "SECRET_KEY não definida no .env! Use uma chave segura em produção."
            )


settings = Settings()

if not settings.SECRET_KEY:
    import secrets
    settings.SECRET_KEY = secrets.token_hex(32)
    logger.warning("SECRET_KEY gerada automaticamente (não persistirá entre reinicializações).")