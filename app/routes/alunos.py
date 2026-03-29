import logging
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.routes.auth import get_current_user
from app.models.usuario import Usuario
from app.services import aluno_service

router = APIRouter(prefix="/alunos", tags=["Alunos"])
logger = logging.getLogger(__name__)


def _redireciona_se_nao_logado(user: Usuario | None):
    """Retorna um RedirectResponse se o usuário não estiver autenticado."""
    if not user:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return None


# ─── LISTAR ────────────────────────────────────────────────────────────────────

@router.get("/web")
def listar_alunos(
    request: Request,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    redirect = _redireciona_se_nao_logado(user)
    if redirect:
        return redirect

    alunos = aluno_service.listar_alunos(db, user_id=user.id)
    return request.app.templates.TemplateResponse(
        "alunos.html",
        {"request": request, "alunos": alunos, "usuario": user},
    )


# ─── DASHBOARD ─────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    redirect = _redireciona_se_nao_logado(user)
    if redirect:
        return redirect

    todos = aluno_service.listar_alunos(db, user_id=user.id)
    ultimos = todos[:5]

    return request.app.templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": user,
            "total": len(todos),
            "ultimos": ultimos,
        },
    )


# ─── FORMULÁRIO DE CADASTRO ────────────────────────────────────────────────────

@router.get("/form")
def form_aluno(
    request: Request,
    user: Usuario = Depends(get_current_user),
):
    redirect = _redireciona_se_nao_logado(user)
    if redirect:
        return redirect

    return request.app.templates.TemplateResponse(
        "form_aluno.html",
        {"request": request, "usuario": user},
    )


# ─── CRIAR ─────────────────────────────────────────────────────────────────────

@router.post("/web")
def criar_aluno(
    request: Request,
    nome: str = Form(...),
    telefone: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    redirect = _redireciona_se_nao_logado(user)
    if redirect:
        return redirect

    aluno_service.criar_aluno(
        db=db,
        nome=nome,
        telefone=telefone,
        user_id=user.id,
        foto=foto,
    )
    return RedirectResponse(url="/alunos/web", status_code=status.HTTP_303_SEE_OTHER)


# ─── EDITAR ────────────────────────────────────────────────────────────────────

@router.get("/editar/id/{aluno_id}")
def form_editar_aluno(
    aluno_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    redirect = _redireciona_se_nao_logado(user)
    if redirect:
        return redirect

    aluno = aluno_service.buscar_aluno(db, aluno_id=aluno_id, user_id=user.id)
    if not aluno:
        return RedirectResponse(url="/alunos/web", status_code=status.HTTP_303_SEE_OTHER)

    return request.app.templates.TemplateResponse(
        "editar_aluno.html",
        {"request": request, "aluno": aluno, "usuario": user},
    )


@router.post("/editar/id/{aluno_id}")
def editar_aluno(
    aluno_id: int,
    nome: str = Form(...),
    telefone: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    redirect = _redireciona_se_nao_logado(user)
    if redirect:
        return redirect

    aluno_service.atualizar_aluno(
        db=db,
        aluno_id=aluno_id,
        user_id=user.id,
        nome=nome,
        telefone=telefone,
        foto=foto,
    )
    return RedirectResponse(url="/alunos/web", status_code=status.HTTP_303_SEE_OTHER)


# ─── DELETAR (via POST para evitar CSRF) ───────────────────────────────────────

@router.post("/deletar/id/{aluno_id}")
def deletar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    redirect = _redireciona_se_nao_logado(user)
    if redirect:
        return redirect

    aluno_service.deletar_aluno(db, aluno_id=aluno_id, user_id=user.id)
    return RedirectResponse(url="/alunos/web", status_code=status.HTTP_303_SEE_OTHER)
