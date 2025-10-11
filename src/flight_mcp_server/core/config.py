from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    GOOGLE_API_KEY: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    RAPIDAPI_API_KEY: str
    RAPIDAPI_BASE_URL: str
    LANGSMITH_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

config = Config()