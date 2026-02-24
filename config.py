from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/jewelry_db"
    GEMINI_API_KEY: str = ""
    SECRET_KEY: str = "your_super_secret_key_for_jwt_token_generation_change_this_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
