import os
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from app.dynamo_service import DynamoService

app = FastAPI(title="URL Shortener API")
db = DynamoService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Reemplazar con URL de S3 en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = os.getenv("BASE_URL", "http://localhost") # URL pública de EC2 o Dominio

class URLRequest(BaseModel):
    original_url: HttpUrl

@app.post("/shorten", status_code=201)
def shorten_url(req: URLRequest):
    try:
        item = db.create_link(str(req.original_url))
        return {
            "short_code": item["short_code"],
            "original_url": item["original_url"],
            "short_url": f"{BASE_URL}/{item['short_code']}"
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    item = db.get_link(short_code)
    if not item:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    return RedirectResponse(url=item["original_url"], status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@app.get("/urls/{short_code}")
def get_info(short_code: str):
    item = db.get_link(short_code)
    if not item:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    return item