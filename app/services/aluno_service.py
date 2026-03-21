from sqlalchemy.orm import Session
from app.models.aluno import Aluno
import uuid
import os


# 🔹 Função para salvar foto
def salvar_foto(foto):
    if not foto:
        return None

    # Validar tipo de arquivo
    extensoes_permitidas = ["image/jpeg", "image/png"]
    if foto.content_type not in extensoes_permitidas:
        return None

    # Nome único
    filename = f"{uuid.uuid4()}_{foto.filename}"

    # Pasta organizada
    pasta = "app/static/uploads/alunos"
    os.makedirs(pasta, exist_ok=True)

    path = f"{pasta}/{filename}"

    # Salvar arquivo
    with open(path, "wb") as f:
        f.write(foto.file.read())

    return f"/static/uploads/alunos/{filename}"


# 🔹 Criar aluno
def criar_aluno(db: Session, nome: str, telefone: str, foto=None):
    caminho_foto = salvar_foto(foto)

    aluno = Aluno(
        nome=nome,
        telefone=telefone,
        foto=caminho_foto
    )

    db.add(aluno)
    db.commit()
    db.refresh(aluno)

    return aluno


# 🔹 Listar alunos
def listar_alunos(db: Session):
    return db.query(Aluno).order_by(Aluno.id.desc()).all()


# 🔹 Buscar aluno por ID
def buscar_aluno(db: Session, aluno_id: int):
    return db.query(Aluno).filter(Aluno.id == aluno_id).first()


# 🔹 Deletar aluno
def deletar_aluno(db: Session, aluno_id: int):
    aluno = buscar_aluno(db, aluno_id)

    if not aluno:
        return None

    db.delete(aluno)
    db.commit()

    return True


# 🔹 Atualizar aluno
def atualizar_aluno(db: Session, aluno_id: int, nome: str, telefone: str):
    aluno = buscar_aluno(db, aluno_id)

    if not aluno:
        return None

    aluno.nome = nome
    aluno.telefone = telefone

    db.commit()
    db.refresh(aluno)

    return aluno