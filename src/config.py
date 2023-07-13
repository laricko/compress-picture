from os import environ

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_password: str = environ["POSTGRES_PASSWORD"]
    postgres_db: str = environ["POSTGRES_DB"]
    postgres_user: str = environ["POSTGRES_USER"]
    db_url: str = (
        f"postgresql://{postgres_user}:{postgres_password}@db:5432/{postgres_db}"
    )
    resizing_tasks_allowed_amount: int = environ["resizing_tasks_allowed_amount"]


settings = Settings()
