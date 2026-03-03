from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    URL : str
    OTP_EXPIRE_MINUTES : int
    SECRET_KEY : str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_DAYS: int
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    CREATE_RESET_TOKEN_MINUTES:int
    
    class Config:
        env_file = ".env"
        
        
settings = Settings()
    
