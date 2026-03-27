from pydantic import BaseModel
from typing import Optional


class AlunoBase(BaseModel):
    nome: str
    telefone: str


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(BaseModel):
    nome: str
    telefone: str


class AlunoResponse(AlunoBase):
    id: int
    foto: Optional[str] = None
    user_id: int

    class Config:
        from_attributes = True
