from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "hr_interview"
    RETELL_API_KEY: str = "key_a39793c1ec275256ccefc270dfb2"
    BASE_URL: str = "http://localhost:8000"  # Base URL for API endpoints in deployment
    GENERATE_CODE_BASE_URL: str = "http://localhost:8000"
    INTERVIEW_FRONTEND_URL: str = "http://localhost:8000/interview.html"
    
    # JWT Authentication Settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
