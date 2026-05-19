from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routers import estudiante
from app.routers.nota import router as notas_router
from app.routers.materia import router as materia_router
from app.routers.evento_evaluativo import router as evento_router

from app.routers.meta import router as meta_router

app = FastAPI()  # ← Primero se crea la app

app.include_router(meta_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(estudiante.router)
app.include_router(notas_router)
app.include_router(materia_router)
app.include_router(evento_router)

# Archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/")
def test():
    return {"ok": True}