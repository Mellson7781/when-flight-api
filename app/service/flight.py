from app.infrastructure.redis import RedisCache
from app.infrastructure.external_api import ExternalAPI 
from app.schemas.flight import Flight, AiroportDelay, OutForescast
from app.common.lifetime import LifeTime
from app.common.types import AiroportCodeType, StatusType
from app.error.flight import LittleDate

from datetime import date, timedelta, timezone,  datetime
import asyncio


class FlightService:
    def __init__(self, redis: RedisCache, external_api: ExternalAPI):
        self.redis = redis
        self.external_api = external_api

    async def searech(self, number: str, localDate: date) -> Flight:
        key = f"flight:{number}:{localDate}"
        flight = await self.redis.get(key)

        if flight is None:
            flight = await self._searech_external_api(number, localDate)
        elif isinstance(flight, dict):
            flight = Flight.model_validate(flight)
        
        return flight

    async def forescast(self, number: str, localDate: date) -> OutForescast:
        flight = await self.searech(number, localDate)

        if flight.departure_iata is None or flight.arrival_iata is None:
            raise LittleDate()

        departuresDelayInfo = await self._get_delay_info(flight.departure_iata)
        arrivalsDelayInfo = await self._get_delay_info(flight.arrival_iata)
        
        driff = flight.departure_revisedTime_utc - datetime.now(timezone.utc)       

        if driff > timedelta(hours=6):
            raise LittleDate()
        
        departures_delay = await self._probability_of_delay(departuresDelayInfo)
        arrivals_delay = await self._probability_of_delay(arrivalsDelayInfo)
        
        if departures_delay >= arrivals_delay:
            delay_index = departures_delay
        else:
            delay_index = arrivals_delay
        
        if delay_index == 0.0:
            raise LittleDate()
        elif delay_index < 1.0:
            delay = StatusType.LOW
        elif delay_index < 3.0:
            delay = StatusType.MEDIUM
        else:
            delay = StatusType.HIGh

        return OutForescast(departure_airoport=departuresDelayInfo, arrival_airoport=arrivalsDelayInfo, chance_of_delay=delay)


    async def _searech_external_api(self, number: str, localDate: date) -> Flight:
        flight = await self.external_api.get_data_flight(number, localDate)
        flight = Flight.model_validate(flight)
        await asyncio.sleep(1)

        key = f"flight:{number}:{localDate}"
        await self.redis.set(key, flight.model_dump(mode='json'), ttl=LifeTime.FLIGHT.value)
        
        return flight
    
    async def _get_delay_info(self, code: str) -> AiroportDelay:
        key = f"forescast:{code}"

        delayInfo = await self.redis.get(key)

        if delayInfo is None:
            delayInfo = await self.external_api.get_delay_info(AiroportCodeType.IATA, code)
            await self.redis.set(key, delayInfo.model_dump(mode="json"), ttl=LifeTime.FLIGHT.value)
            await asyncio.sleep(1)
        else:
            delayInfo = AiroportDelay.model_validate(delayInfo)

        return delayInfo
            
    async def _finding_the_average(self, toDelay: float, fromDelay: float) -> float:
        return (toDelay + fromDelay) / 2
    
    async def _probability_of_delay(self, delayInfo: AiroportDelay):
        delay_index = await self._finding_the_average(delayInfo.departuresDelayInformation.delayIndex, delayInfo.arrivalsDelayInformation.delayIndex)
        return delay_index