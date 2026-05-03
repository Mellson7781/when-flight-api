from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.redis import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis
    print("Redis connection")
    yield
    await app.state.redis.aclose()
    print("Redis close connection")