from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

# Create a single engine instance at import time (thread-safe)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # set to True for SQL debug logs
    pool_pre_ping=True,
    future=True,
)

# Use async_sessionmaker instead of sessionmaker (clearer API in SQLAlchemy 2.x)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Dependency for FastAPI routes
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # Ensure session is closed properly, even if exceptions occur
            await session.close()
