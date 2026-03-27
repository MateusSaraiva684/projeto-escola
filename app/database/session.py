from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não definida. Configure o arquivo .env com a URL do PostgreSQL.\n"
        "Exemplo: DATABASE_URL=postgresql://usuario:senha@host:5432/escola"
    )

# psycopg3 requer o prefixo postgresql+psycopg://
# Aceita tanto postgresql:// quanto postgres:// (formato do Render)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

_is_local = any(h in DATABASE_URL for h in ("localhost", "127.0.0.1"))
connect_args = {} if _is_local else {"sslmode": "require"}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
