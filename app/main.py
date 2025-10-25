from fastapi import FastAPI
from app.api.routes import shorten, redirect
from app.db.init_db import init_db

app = FastAPI(title="URL Shortener")

app.include_router(shorten.router)
app.include_router(redirect.router)

@app.on_event("startup")
async def on_startup():
    await init_db()