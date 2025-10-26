from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.db.models import Url
from app.services.shortener import generate_short_code
from app.services.cache import set_cached_url

router = APIRouter(prefix="/api/shorten", tags=["Shorten"])

class ShortenRequest(BaseModel):
    original_url: HttpUrl

class ShortenResponse(BaseModel):
    short_code: str
    short_url: str

@router.post("/", response_model=ShortenResponse)
async def create_short_url(payload: ShortenRequest, db: AsyncSession = Depends(get_session)):
    """Create a short URL for a given original URL."""
    original_url = str(payload.original_url)  # ✅ Convert HttpUrl → str

    # 1️⃣ Check if URL already exists
    existing = await db.execute(select(Url).where(Url.original_url == original_url))
    existing_url = existing.scalar_one_or_none()

    if existing_url:
        short_url = f"http://localhost:8000/r/{existing_url.short_code}"
        return ShortenResponse(short_code=existing_url.short_code, short_url=short_url)

    # 2️⃣ Generate new short code
    short_code = generate_short_code()

    # 3️⃣ Store in DB
    new_url = Url(short_code=short_code, original_url=original_url)
    db.add(new_url)
    await db.commit()

    # 4️⃣ Cache it
    await set_cached_url(short_code, original_url)

    # 5️⃣ Return the short URL
    short_url = f"http://localhost:8000/r/{short_code}"
    return ShortenResponse(short_code=short_code, short_url=short_url)
