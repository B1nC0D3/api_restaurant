from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    allowed_origins: set


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
