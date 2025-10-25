from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

router = APIRouter(prefix="/api/shorten", tags=["Shorten"])

@router.post("/")
async def create_short_url(original_url: str, db: AsyncSession = Depends(get_session)):
    # temporary stub
    return {"message": f"Received {original_url}"}
