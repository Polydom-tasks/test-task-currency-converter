from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:password@localhost/currencydb"
    exchangeratesapi_token: str = "token"

    class Config:
        env_file = ".env"


settings = Settings()
