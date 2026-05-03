from fastapi import APIRouter

from app.core.tags import Tags


ping_rt = APIRouter(prefix="/api/ping", tags=[Tags.SYSTEM])


@ping_rt.get("/")
async def ping():
    return {"message": "pong"}