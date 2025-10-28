from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

        model_config = SettingsConfigDict(
            env_file = ".env",
            extra="ignore")
        

Config = Settings()