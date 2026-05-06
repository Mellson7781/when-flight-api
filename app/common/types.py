from enum import Enum


class AiroportCodeType(Enum):
    IATA = "iata"
    ICAO = "icao"


class StatusType(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGh = "high"