from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.usuario import Usuario

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# 📄 Página login
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 🔐 Processar login
@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.email == email).first()

    if not user or user.senha != senha:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "erro": "Email ou senha inválidos"
        })

    # login ok
    return templates.TemplateResponse("alunos.html", {
        "request": request,
        "alunos": []
    })