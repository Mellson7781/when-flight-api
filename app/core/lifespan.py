from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.redis import redis
from app.core.external import external_conection


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis
    print("Redis connection")
    app.state.external = external_conection
    print("External connection")
    yield
    await app.state.redis.aclose()
    print("Redis close connection")
    await app.state.external.aclose()
    print("External close connection")