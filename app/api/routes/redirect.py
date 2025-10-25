from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_session
from app.db.models import Url
from app.services.cache import get_cached_url, set_cached_url

router = APIRouter(prefix="/r", tags=["Redirect"])

@router.get("/{short_code}")
async def redirect_to_url(short_code: str, db: AsyncSession = Depends(get_session)):
    # 1️⃣ Check cache first (fast path)
    cached_url = await get_cached_url(short_code)
    if cached_url:
        return RedirectResponse(url=cached_url, status_code=307)

    # 2️⃣ Fallback to database lookup
    result = await db.execute(select(Url).where(Url.short_code == short_code))
    url_obj = result.scalar_one_or_none()

    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")

    # 3️⃣ Cache it for next time
    await set_cached_url(short_code, url_obj.original_url)

    # 4️⃣ Optionally update analytics (click count, last access, etc.)
    url_obj.clicks += 1
    await db.commit()

    return RedirectResponse(url=url_obj.original_url, status_code=307)
