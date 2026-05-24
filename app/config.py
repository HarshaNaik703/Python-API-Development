from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY:str
    EXPIRATION_TIME:int
    ALGORITHM :str
    DATABASE_URL:str
    
    class Config:
        env_file = ".env"

settings = Settings()

