import httpx

from app.core.config import settings

external_conection = httpx.AsyncClient(
    timeout=httpx.Timeout(15.0, connect=5.0),
    headers={
        "X-RapidAPI-Key": settings.RapidAPI_Key,
        "X-RapidAPI-Host": settings.RapidAPI_Host
        }
)