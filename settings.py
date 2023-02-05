from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    allowed_origins: set
    redis_path: str
    rabbitmq_path: str


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
