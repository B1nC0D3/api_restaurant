from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
