from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database.connection import get_db
from app.services import aluno_service
from app.models.aluno import Aluno

router = APIRouter(prefix="/alunos")
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


# 🔹 API - Listar alunos (CORREÇÃO AQUI)
@router.get("/api")
def listar_api(db: Session = Depends(get_db)):
    return aluno_service.listar_alunos(db)


# 🔹 WEB - Página de alunos
@router.get("/web")
def pagina_alunos(request: Request, db: Session = Depends(get_db)):
    alunos = aluno_service.listar_alunos(db)
    return templates.TemplateResponse("alunos.html", {
        "request": request,
        "alunos": alunos
    })


# 🔹 WEB - Formulário
@router.get("/form")
def form_aluno(request: Request):
    return templates.TemplateResponse("form_aluno.html", {"request": request})


# 🔹 WEB - Criar aluno
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


# 🔹 WEB - Deletar
@router.get("/deletar/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if aluno:
        db.delete(aluno)
        db.commit()

    return RedirectResponse(url="/alunos/web", status_code=303)


# 🔹 WEB - Form editar
@router.get("/editar/{aluno_id}")
def editar_aluno_form(aluno_id: int, request: Request, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    return templates.TemplateResponse("editar_aluno.html", {
        "request": request,
        "aluno": aluno
    })


# 🔹 WEB - Atualizar
@router.post("/editar/{aluno_id}")
def editar_aluno(
    aluno_id: int,
    nome: str = Form(...),
    telefone: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if aluno:
        aluno.nome = nome
        aluno.telefone = telefone

        if foto:
            caminho_foto = aluno_service.salvar_foto(foto)
            aluno.foto = caminho_foto

        db.commit()

    return RedirectResponse(url="/alunos/web", status_code=303)