from pydantic import BaseSettings


class Settings(BaseSettings):

    database_url: str
    allowed_origins: set
    jwt_secret: str = 'super_secret'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 1


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
