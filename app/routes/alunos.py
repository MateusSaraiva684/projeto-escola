from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.aluno import Aluno
from app.routes.auth import get_current_user

router = APIRouter(prefix="/alunos", tags=["Alunos"])


# 🔒 LISTAR ALUNOS (PROTEGIDO)
@router.get("/")
def listar_alunos(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    
    if not user:
        return RedirectResponse(url="/")

    alunos = db.query(Aluno).all()

    return request.app.templates.TemplateResponse(
        "alunos.html",
        {
            "request": request,
            "alunos": alunos,
            "usuario": user
        }
    )


# ➕ CRIAR ALUNO (PROTEGIDO)
@router.post("/criar")
def criar_aluno(
    request: Request,
    nome: str = Form(...),
    idade: int = Form(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user:
        return RedirectResponse(url="/")

    novo_aluno = Aluno(
        nome=nome,
        idade=idade
    )

    db.add(novo_aluno)
    db.commit()

    return RedirectResponse(url="/alunos", status_code=302)


# ❌ DELETAR ALUNO (PROTEGIDO)
@router.get("/deletar/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    
    if not user:
        return RedirectResponse(url="/")

    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if aluno:
        db.delete(aluno)
        db.commit()

    return RedirectResponse(url="/alunos", status_code=302)