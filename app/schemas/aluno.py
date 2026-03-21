from pydantic import BaseModel

class AlunoBase(BaseModel):
    nome: str
    telefone: str

class AlunoCreate(AlunoBase):
    pass

class AlunoResponse(AlunoBase):
    id: int
    foto: str | None

    class Config:
        from_attributes = True