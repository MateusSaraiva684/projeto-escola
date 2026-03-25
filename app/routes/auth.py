from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.usuario import Usuario
from app.core.security import (
    hash_senha,
    verificar_senha,
    criar_token
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

    if not user or not verificar_senha(senha, user.senha):
        return RedirectResponse(
            url="/?erro=1",
            status_code=status.HTTP_303_SEE_OTHER
        )

    token = criar_token({"user_id": user.id})

    response = RedirectResponse(
        url="/alunos/",
        status_code=status.HTTP_303_SEE_OTHER
    )

    # ✅ COOKIE CORRIGIDO (PONTO PRINCIPAL)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        path="/",
        secure=False  # importante para ambiente sem HTTPS estrito
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
        return RedirectResponse(
            url="/?erro=email_existe",
            status_code=status.HTTP_303_SEE_OTHER
        )

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=hash_senha(senha)
    )

    db.add(novo_usuario)
    db.commit()

    return RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER
    )


# 🚪 LOGOUT
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")

    response.delete_cookie(
        key="access_token",
        path="/"  # 🔥 garante que apaga corretamente
    )

    return response


# 🔒 USUÁRIO ATUAL (AUTH)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        print("❌ Sem token no cookie")
        return None

    try:
        from jose import jwt
        from app.core.config import settings

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        print("✅ TOKEN DECODIFICADO:", payload)

    except Exception as e:
        print("❌ ERRO AO DECODIFICAR TOKEN:", e)
        return None

    user = db.query(Usuario).filter(
        Usuario.id == payload.get("user_id")
    ).first()

    if not user:
        print("❌ Usuário não encontrado no banco")

    return user