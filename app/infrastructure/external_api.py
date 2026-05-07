from datetime import date

from app.error.external import ExternalHTTPStatusError
from app.error.flight import NotFoundFlight
from app.schemas.external import ExternalFlight
from app.schemas.flight import AiroportDelay
from app.common.types import AiroportCodeType

import httpx


class ExternalAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    #GET /flights/number/LH1234?date=2026-03-30
    async def get_data_flight(self, number: str, date: date) -> ExternalFlight:
        url = f"https://aerodatabox.p.rapidapi.com/flights/number/{number}"
        params = {"date": date}
        try:
            response = await self.client.get(url, params=params)

            if response.status_code == 204:
                raise NotFoundFlight()
            
            response.raise_for_status()
        except httpx.RequestError:
            raise ExternalHTTPStatusError(status_code=502)
        except httpx.HTTPStatusError as e:
            raise ExternalHTTPStatusError(status_code=e.response.status_code)

        result_api = response.json()

        if not isinstance(result_api, list) or not result_api:
            raise NotFoundFlight()

        if not isinstance(result_api[0], dict):
            raise ExternalHTTPStatusError(status_code=502)
        
        result_api = result_api[0]

        try:
            flight = ExternalFlight(
                number=result_api.get("number"),
                status=result_api.get("status"),
                aircraft=result_api.get("aircraft", {}).get("model"),

                departure_iata=result_api.get("departure", {}).get("airport", {}).get("iata"),
                departure_scheduledTime=result_api.get("departure", {}).get("scheduledTime", {}).get("local"),
                departure_scheduledTime_utc=result_api.get("departure", {}).get("scheduledTime", {}).get("utc"),
                departure_municipality = result_api.get("departure", {}).get("municipality"),
                departure_revisedTime = result_api.get("departure", {}).get("revisedTime", {}).get("local"),
                departure_revisedTime_utc = result_api.get("departure", {}).get("revisedTime", {}).get("utc"),

                arrival_iata=result_api.get("arrival", {}).get("airport", {}).get("iata"),
                arrival_scheduledTime=result_api.get("arrival", {}).get("scheduledTime", {}).get("local"),
                arrival_scheduledTime_utc=result_api.get("arrival", {}).get("scheduledTime", {}).get("utc"),
                arrival_municipality = result_api.get("arrival", {}).get("municipality"),
                arrival_revisedTime = result_api.get("arrival", {}).get("revisedTime", {}).get("local"),
                arrival_revisedTime_utc = result_api.get("arrival", {}).get("revisedTime", {}).get("utc"),

                local_date=result_api.get("departure", {}).get("scheduledTime", {}).get("local"),
                airline=result_api.get("airline", {}).get("name")
            )        

            if flight.local_date is None or flight.local_date != date:
                raise NotFoundFlight()
            
            return flight
        except ValueError:
            raise ExternalHTTPStatusError(status_code=422)
    

    async def get_delay_info(self, codetype: AiroportCodeType, code: str) -> AiroportDelay:
        url = f"https://aerodatabox.p.rapidapi.com/airports/{codetype.value}/{code}/delays"
        params = {
            "code": code,
            "codeType": codetype.value
        }

        try:
            response = await self.client.get(url, params=params)

            if response.status_code == 204:
                raise ExternalHTTPStatusError(status_code=404)
            
            response.raise_for_status()
        except httpx.RequestError:
            raise ExternalHTTPStatusError(status_code=502)
        except httpx.HTTPStatusError as e:
            raise ExternalHTTPStatusError(status_code=e.response.status_code)

        result_api = response.json()

        if not isinstance(result_api, dict):
            raise ExternalHTTPStatusError(status_code=502)
        
        result = AiroportDelay.model_validate(result_api)

        return result