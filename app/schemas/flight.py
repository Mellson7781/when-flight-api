from pydantic import BaseModel, field_validator
from datetime import date, datetime


class QueryFilters(BaseModel):
    number: str
    LocalDate: date

    @field_validator("number")
    def validate_number(cls, v: str):
        v = v.upper()

        if len(v) <= 2:
            raise ValueError()
        
        if v[2] == "-":
           v = v.replace("-", " ") 
        elif v[2] != " ":
            v = v[:2] + " " + v[2:]
        
        return v


class OutFlight(BaseModel):
    number: str
    status: str | None
    aircraft: str | None

    departure_iata: str | None
    departure_scheduledTime: datetime
    departure_municipality: str | None
    departure_revisedTime: datetime | None

    arrival_iata: str | None
    arrival_scheduledTime: datetime
    arrival_municipality: str | None
    arrival_revisedTime: datetime | None

    airline: str | None
    local_date: date | None

    model_config = {
        "from_attributes": True
    }