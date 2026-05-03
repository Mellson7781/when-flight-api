from fastapi import Request, Depends

from typing import Annotated

from app.service.flight import FlightService
from app.infrastructure.redis import RedisCache
from app.infrastructure.external_api import ExternalAPI


async def get_redis(request: Request):
    return request.app.state.redis


async def get_external(request: Request):
    return request.app.state.external


async def get_service(
    external: Annotated[ExternalAPI, Depends(get_external)],
    redis: Annotated[RedisCache, Depends(get_redis)]
):
    return FlightService(
        redis=RedisCache(redis),
        external_api=ExternalAPI(external)
    )