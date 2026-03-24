from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.session import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)
    telefone = Column(String)
    foto = Column(String)

    # 🔐 vínculo com usuário (ESSENCIAL)
    user_id = Column(Integer, ForeignKey("usuarios.id"))