from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Charity fund'
    description: str = 'Charity fun API-service'
    database_url: str = 'sqlite+aiosqlite:///./charity_fund.db'
    secret: str = 'SECRET_KEY'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    minimum_investing_sum = 0

    class Config:
        env_file = '.env'


settings = Settings()
