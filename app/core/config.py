import os
from typing import List
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/blood_donor_db"
    )
    database_host: str = os.getenv("DATABASE_HOST", "localhost")
    database_port: int = int(os.getenv("DATABASE_PORT", "5432"))
    database_name: str = os.getenv("DATABASE_NAME", "blood_donor_db")
    database_user: str = os.getenv("DATABASE_USER", "user")
    database_password: str = os.getenv("DATABASE_PASSWORD", "password")

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
    allowed_origins: List[str] = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:3000"
    ).split(",")

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = os.getenv("LOG_FORMAT", "json")

    # Rate Limiting
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))


settings = Settings()
