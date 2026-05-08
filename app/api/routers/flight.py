from fastapi import APIRouter, Depends, Query, HTTPException

from typing import Annotated

from app.core.tags import Tags
from app.schemas.flight import QueryFilters, Flight
from app.service.flight import FlightService
from app.dependencies.flight import get_service

from app.error.external import ExternalHTTPStatusError
from app.error.flight import NotFoundFlight, LittleDate


flight_rt = APIRouter(prefix="/api/flight", tags=[Tags.FLIGHT])


@flight_rt.get("/search/number", response_model=Flight)
async def get_flight(
    filters_query: Annotated[QueryFilters, Query()],
    service: Annotated[FlightService, Depends(get_service)]
):
    try:
        return await service.searech(number=filters_query.number, localDate=filters_query.LocalDate)
    except ExternalHTTPStatusError as e:
        raise HTTPException(status_code=e.status_code, detail="External_Api")
    except NotFoundFlight:
        raise HTTPException(status_code=404, detail="Flight not found")
    

@flight_rt.get("/forecast")
async def forescast_flight(
    filters_query: Annotated[QueryFilters, Query()],
    service: Annotated[FlightService, Depends(get_service)]
):
    try:
        return await service.forescast(number=filters_query.number, localDate=filters_query.LocalDate)
    except ExternalHTTPStatusError as e:
        raise HTTPException(status_code=e.status_code, detail="External_Api")
    except LittleDate:
        raise HTTPException(status_code=400, detail="Too little data to make a forecast")
    except NotFoundFlight:
        raise HTTPException(status_code=404, detail="Flight not found")