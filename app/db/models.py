from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(12), unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
