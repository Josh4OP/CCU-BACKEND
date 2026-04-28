from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import estudiante

app = FastAPI()

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