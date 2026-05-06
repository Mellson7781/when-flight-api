from pydantic import BaseModel, field_validator, Field
from datetime import date, datetime, timedelta

from app.common.types import StatusType

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


class Flight(BaseModel):
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

    model_config = {
        "from_attributes": True
    }

class TimeInfo(BaseModel):
    utc: datetime
    local: datetime

    @field_validator("utc", "local", mode="before")
    @classmethod
    def parse_time(cls, v):
        # убираем Z / timezone мусор
        if isinstance(v, str):
            v = v.replace("Z", "")
        return datetime.fromisoformat(v)


class DelayInformation(BaseModel):
    numTotal: int | None = None
    numQualifiedTotal: int | None = None
    numCancelled: int | None = None
    medianDelay: timedelta | None = None
    delayIndex: float = 0.0


class AiroportDelay(BaseModel):
    airportIcao: str
    from_: TimeInfo = Field(alias="from")
    to: TimeInfo
    departuresDelayInformation: DelayInformation
    arrivalsDelayInformation: DelayInformation

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class OutForescast(BaseModel):
    chance_of_delay: StatusType
    departure_airoport: AiroportDelay
    arrival_airoport: AiroportDelay