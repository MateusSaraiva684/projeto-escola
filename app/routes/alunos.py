from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database.session import get_db
from app.services import aluno_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# 🔹 API - Criar aluno
@router.post("/")
def criar(
    nome: str = Form(...),
    telefone: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return aluno_service.criar_aluno(db, nome, telefone, foto)


# 🔹 API - Listar alunos
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return aluno_service.listar_alunos(db)


# 🔹 WEB - Página de alunos
@router.get("/web")
def pagina_alunos(request: Request, db: Session = Depends(get_db)):
    alunos = aluno_service.listar_alunos(db)
    return templates.TemplateResponse("alunos.html", {
        "request": request,
        "alunos": alunos
    })


# 🔹 WEB - Formulário de criação
@router.get("/form")
def form_aluno(request: Request):
    return templates.TemplateResponse("form_aluno.html", {"request": request})


# 🔹 WEB - Criar aluno via formulário
@router.post("/web")
def criar_web(
    request: Request,
    nome: str = Form(...),
    telefone: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    aluno_service.criar_aluno(db, nome, telefone, foto)

    return RedirectResponse(url="/alunos/web", status_code=303)


# 🔹 WEB - Deletar aluno
@router.get("/deletar/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno_service.deletar_aluno(db, aluno_id)
    return RedirectResponse(url="/alunos/web", status_code=303)


# 🔹 WEB - Form editar aluno
@router.get("/editar/{aluno_id}")
def editar_aluno_form(aluno_id: int, request: Request, db: Session = Depends(get_db)):
    aluno = aluno_service.buscar_aluno(db, aluno_id)

    return templates.TemplateResponse("editar_aluno.html", {
        "request": request,
        "aluno": aluno
    })


# 🔹 WEB - Atualizar aluno
@router.post("/editar/{aluno_id}")
def editar_aluno(
    aluno_id: int,
    nome: str = Form(...),
    telefone: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    aluno = aluno_service.buscar_aluno(db, aluno_id)

    if aluno:
        if foto:
            caminho_foto = aluno_service.salvar_foto(foto)
            aluno.foto = caminho_foto

        aluno_service.atualizar_aluno(db, aluno_id, nome, telefone)

    return RedirectResponse(url="/alunos/web", status_code=303)