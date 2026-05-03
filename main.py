from fastapi import FastAPI
import uvicorn

from app.core.config import settings
from app.api.routers.ping import ping_rt
from app.core.lifespan import lifespan


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)


app.include_router(ping_rt)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)