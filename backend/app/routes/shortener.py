from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.models.schemas import CreateLinkRequest, ShortLinkResponse, LinkNotFoundError
from app.services import dynamo_services

router = APIRouter()

@router.post("/shorten", response_model=ShortLinkResponse,
             status_code=status.HTTP_201_CREATED)
async def shorten(req:
