from sqlalchemy import Column, Integer, String
from app.database.session import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    telefone = Column(String)
    foto = Column(String)