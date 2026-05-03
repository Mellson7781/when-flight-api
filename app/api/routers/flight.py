from fastapi import APIRouter, Depends, Query, HTTPException

from typing import Annotated

from app.core.tags import Tags
from app.schemas.flight import QueryFilters, OutFlight
from app.service.flight import FlightService
from app.dependencies.flight import get_service

from app.error.external import ExternalHTTPStatusError
from app.error.flight import NotFoundFlight


flight_rt = APIRouter(prefix="/api/filght", tags=[Tags.FLIGHT])


@flight_rt.get("/searech/number/", response_model=OutFlight)
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