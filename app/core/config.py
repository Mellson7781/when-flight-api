from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    APP_NAME: str 
    DEBUG: bool
    DESCRIPTION: str
    VERSION: str

    HOST: str
    PORT: int

    RapidAPI_Key: str
    RapidAPI_Host: str = "aerodatabox.p.rapidapi.com"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str


settings = Settings() 