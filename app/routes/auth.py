from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.usuario import Usuario
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

router = APIRouter()


# 🔐 LOGIN
@router.post("/login")
def login(
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.email == email).first()

    if not user or not verify_password(senha, user.senha):
        return RedirectResponse(url="/?erro=1", status_code=status.HTTP_302_FOUND)

    token = create_access_token({"user_id": user.id})

    response = RedirectResponse(url="/alunos", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,      # 🔒 importante no Render (HTTPS)
        samesite="lax"
    )

    return response


# 📝 REGISTRO
@router.post("/registrar")
def registrar(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    user_existente = db.query(Usuario).filter(Usuario.email == email).first()

    if user_existente:
        return RedirectResponse(url="/?erro=email_existe", status_code=302)

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=hash_password(senha)
    )

    db.add(novo_usuario)
    db.commit()

    return RedirectResponse(url="/", status_code=302)


# 🚪 LOGOUT
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


# 🔒 DEPENDÊNCIA DE AUTENTICAÇÃO
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        return None

    payload = verify_token(token)

    if not payload:
        return None

    user = db.query(Usuario).filter(Usuario.id == payload.get("user_id")).first()

    return user