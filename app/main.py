from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import estudiante

app = FastAPI()

#Esto es provicional
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, pon tu dominio específico
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "pong"}






# Rutas
app.include_router(estudiante.router)

# Archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Endpoint de prueba
@app.get("/")
def test():
    return {"ok": True}

#Cuando vayas a corres usa: uvicorn app.main:app --reload

"""
{
  "nombre": "Josh Prueba",
  "correo": "josh1@test.com",
  "password": "Test1234"
}
"""
