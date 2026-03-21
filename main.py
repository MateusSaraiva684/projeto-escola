from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database.session import Base, engine
from app.routes import alunos
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 🔹 Static (CSS, imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 🔹 Criar tabelas
Base.metadata.create_all(bind=engine)

# 🔹 Rotas
app.include_router(alunos.router, prefix="/alunos")

# 🔹 Rota inicial (abre a página web)
@app.get("/")
def home():
    return RedirectResponse(url="/alunos/web")
