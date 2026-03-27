import uuid
import os
import logging
from sqlalchemy.orm import Session
from app.models.aluno import Aluno

logger = logging.getLogger(__name__)

EXTENSOES_PERMITIDAS = {"image/jpeg", "image/png", "image/webp"}
TAMANHO_MAXIMO = 5 * 1024 * 1024  # 5 MB


def salvar_foto(foto) -> str | None:
    """Salva a foto do aluno e retorna o caminho relativo, ou None em caso de erro."""
    if not foto or not foto.filename:
        return None

    if foto.content_type not in EXTENSOES_PERMITIDAS:
        logger.warning("Tipo de arquivo não permitido: %s", foto.content_type)
        return None

    conteudo = foto.file.read()

    if len(conteudo) > TAMANHO_MAXIMO:
        logger.warning("Arquivo muito grande: %d bytes", len(conteudo))
        return None

    extensao = foto.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4()}.{extensao}"
    pasta = "app/static/uploads/alunos"
    os.makedirs(pasta, exist_ok=True)
    caminho = f"{pasta}/{filename}"

    with open(caminho, "wb") as f:
        f.write(conteudo)

    return f"/static/uploads/alunos/{filename}"


def criar_aluno(db: Session, nome: str, telefone: str, user_id: int, foto=None) -> Aluno:
    caminho_foto = salvar_foto(foto)
    aluno = Aluno(nome=nome, telefone=telefone, foto=caminho_foto, user_id=user_id)
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno


def listar_alunos(db: Session, user_id: int) -> list[Aluno]:
    """Retorna apenas os alunos do usuário logado."""
    return db.query(Aluno).filter(Aluno.user_id == user_id).order_by(Aluno.id.desc()).all()


def buscar_aluno(db: Session, aluno_id: int, user_id: int) -> Aluno | None:
    """Busca um aluno garantindo que pertence ao usuário logado."""
    return (
        db.query(Aluno)
        .filter(Aluno.id == aluno_id, Aluno.user_id == user_id)
        .first()
    )


def atualizar_aluno(
    db: Session, aluno_id: int, user_id: int, nome: str, telefone: str, foto=None
) -> Aluno | None:
    aluno = buscar_aluno(db, aluno_id, user_id)
    if not aluno:
        return None

    aluno.nome = nome
    aluno.telefone = telefone

    nova_foto = salvar_foto(foto)
    if nova_foto:
        aluno.foto = nova_foto

    db.commit()
    db.refresh(aluno)
    return aluno


def deletar_aluno(db: Session, aluno_id: int, user_id: int) -> bool:
    aluno = buscar_aluno(db, aluno_id, user_id)
    if not aluno:
        return False
    db.delete(aluno)
    db.commit()
    return True