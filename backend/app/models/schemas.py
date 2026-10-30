from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class CreateLinkRequest(BaseModel):
    original_url: HttpUrl
    #         ^^^^^^^ Pydantic valida que sea URL real (http://, https://...)

class ShortLinkResponse(BaseModel):
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime

class LinkNotFoundError(Exception):
    """Custom exception para cuando el code no existe en DynamoDB."""
    pass
