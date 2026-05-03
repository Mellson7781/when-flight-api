from app.infrastructure.redis import RedisCache
from app.infrastructure.external_api import ExternalAPI
from app.schemas.external import ExternalFlight
from app.schemas.flight import OutFlight
from app.common.lifetime import LifeTime

from datetime import date


class FlightService:
    def __init__(self, redis: RedisCache, external_api: ExternalAPI):
        self.redis = redis
        self.external_api = external_api

    async def searech(self, number: str, localDate: date) -> OutFlight:
        key = f"flight:{number}:{localDate}"
        flight = await self.redis.get(key)

        if flight is None:
            flight = await self._searech_external_api(number, localDate)
        elif isinstance(flight, dict):
            flight = OutFlight.model_validate(flight)
        
        return flight

    async def _searech_external_api(self, number: str, localDate: date) -> OutFlight:
        flight = await self.external_api.get_data_flight(number, localDate)
        print(flight)
        flight = OutFlight.model_validate(flight)

        key = f"flight:{number}:{localDate}"
        await self.redis.set(key, flight.model_dump(mode='json'), ttl=LifeTime.FLIGHT.value)
        
        return flight