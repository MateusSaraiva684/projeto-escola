from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database.session import Base, engine
from app.routes import alunos
from fastapi.staticfiles import StaticFiles


app = FastAPI(docs_url=None, redoc_url=None)  # 🔥 remove docs

# 🔹 Static (CSS, imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")



# 🔹 Rotas
app.include_router(alunos.router, prefix="/alunos")

# 🔹 Rota inicial (abre a página web)
@app.get("/")
def home():
    return RedirectResponse(url="/alunos/web")

@app.get("/init-db")
def init_db():
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}    

@app.get("/rotas")
def listar_rotas():
    return [r.path for r in app.routes]