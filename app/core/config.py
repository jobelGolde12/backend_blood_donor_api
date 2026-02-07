import os
import json
from typing import List
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    # Database
    @property
    def database_url(self) -> str:
        """Get database URL from environment variable with error handling."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set. Please configure your database connection.")
        return database_url

    # JWT
    secret_key: str = os.getenv(
        "SECRET_KEY", "your-super-secret-key-change-in-production"
    )
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Application
    app_name: str = os.getenv("APP_NAME", "Blood Donor API")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "production")

    # CORS
    @property
    def allowed_origins(self) -> List[str]:
        origins_str = os.getenv("ALLOWED_ORIGINS", '["http://localhost:3000"]')
        try:
            return json.loads(origins_str)
        except json.JSONDecodeError:
            # Fallback to split if JSON parsing fails
            return origins_str.split(",")

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = os.getenv("LOG_FORMAT", "json")

    # Rate Limiting
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))


settings = Settings()
