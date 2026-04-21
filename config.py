import os


class Config:
    """Base configuration loaded from environment variables."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Build the PostgreSQL connection URI from individual env vars
    DB_USER = os.getenv("POSTGRES_USER", "admin")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")
    DB_HOST = os.getenv("DB_HOST", "db")          # 'db' is the Docker Compose service name
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "gradesdb")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Map string names to config classes for easy selection via env var
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
