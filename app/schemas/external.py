from pydantic import BaseModel, field_validator, Field
from datetime import datetime, date


class ExternalFlight(BaseModel):
    number: str
    status: str | None
    aircraft: str | None

    departure_iata: str | None
    departure_scheduledTime: datetime
    departure_scheduledTime_utc: datetime
    departure_municipality: str | None
    departure_revisedTime: datetime | None
    departure_revisedTime_utc: datetime | None

    arrival_iata: str | None
    arrival_scheduledTime: datetime
    arrival_scheduledTime_utc: datetime
    arrival_municipality: str | None
    arrival_revisedTime: datetime | None
    arrival_revisedTime_utc: datetime | None

    airline: str | None
    local_date: date | None

    @field_validator("local_date", mode="before")
    def parse_date(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v).date()
        return v