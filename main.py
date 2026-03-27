import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database.session import Base, engine
from app.routes import alunos, auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None)

templates = Jinja2Templates(directory="app/templates")
app.templates = templates

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(alunos.router)
app.include_router(auth.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.on_event("startup")
def startup_event():
    """Cria as tabelas no banco ao iniciar a aplicação."""
    Base.metadata.create_all(bind=engine)
    logger.info("Banco de dados inicializado.")