from pydantic import BaseModel, field_validator, model_validator
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
    
    @model_validator(mode="before")
    @classmethod
    def check_required_datetimes(cls, values):
        required_fields = [
            "arrival_scheduledTime",
            "arrival_scheduledTime_utc",
            "departure_scheduledTime",
            "departure_scheduledTime_utc",
        ]

        missing = [f for f in required_fields if values.get(f) is None]

        if missing:
            raise ValueError(
                f"ExternalFlight missing required datetime fields: {', '.join(missing)}"
            )

        return values