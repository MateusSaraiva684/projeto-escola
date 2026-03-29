import logging
from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database.session import get_db
from app.models.usuario import Usuario
from app.core.config import settings
from app.core.security import hash_senha, verificar_senha, criar_token

router = APIRouter()
logger = logging.getLogger(__name__)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Usuario | None:
    """Decodifica o token JWT do cookie e retorna o usuário correspondente."""
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
    except JWTError as e:
        logger.debug("Erro ao decodificar token: %s", e)
        return None

    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        logger.debug("Usuário id=%s não encontrado no banco.", user_id)
    return user


@router.post("/login")
def login(
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verificar_senha(senha, user.senha):
        return RedirectResponse(url="/?erro=credenciais_invalidas", status_code=status.HTTP_303_SEE_OTHER)

    token = criar_token({"user_id": user.id})
    response = RedirectResponse(url="/alunos/web", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        path="/",
        secure=False,  # Mude para True em produção com HTTPS
    )
    return response


@router.post("/registrar")
def registrar(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    if db.query(Usuario).filter(Usuario.email == email).first():
        return RedirectResponse(url="/?erro=email_existe", status_code=status.HTTP_303_SEE_OTHER)

    novo_usuario = Usuario(nome=nome, email=email, senha=hash_senha(senha))
    db.add(novo_usuario)
    db.commit()
    return RedirectResponse(url="/?sucesso=conta_criada", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token", path="/")
    return response
