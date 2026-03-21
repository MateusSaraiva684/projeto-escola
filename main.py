from fastapi import FastAPI
from app.database.session import Base, engine
from app.routes import alunos
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
Base.metadata.create_all(bind=engine)
app.include_router(alunos.router, prefix="/alunos")

@app.get("/")
def home():
    return {"msg": "API funcionando"}