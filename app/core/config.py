from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    # Only the test suite uses this, so the app can still start without it.
    TEST_DATABASE_URL: str | None = None

    # Reads from real environment variables first, then falls back to a local .env file.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore[call-arg]  # required fields are filled from the environment
