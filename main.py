from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.session import Base, engine
from app.routes import alunos
from app.routes import auth

app = FastAPI(docs_url=None, redoc_url=None)

# 🔹 Templates
templates = Jinja2Templates(directory="app/templates")
app.templates = templates

# 🔹 Static (CSS, imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 🔹 Rotas
app.include_router(alunos.router)
app.include_router(auth.router)

# 🔹 Página inicial (LOGIN)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

# 🔹 Inicializar banco (usar uma vez se precisar)
@app.get("/init-db")
def init_db():
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}

# 🔹 Debug de rotas
@app.get("/rotas")
def listar_rotas():
    return [r.path for r in app.routes]

@app.get("/reset-db")
def reset_db():
    Usuario.__table__.drop(engine)
    Usuario.__table__.create(engine)
    return {"status": "resetado"}    