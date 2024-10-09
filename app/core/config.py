from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Note Taking App"
    DATABASE_URL: str = (
        "mongodb+srv://codseed2:Nabeelnasir123@notifier.p6rhi.mongodb.net/?retryWrites=true&w=majority&appName=notifier"
    )
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
