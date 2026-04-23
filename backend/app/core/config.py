from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    FEATHERLESS_API_KEY: str
    FEATHERLESS_BASE_URL: str
    AI_MODEL: str
    CIRCLE_API_KEY: str
    CIRCLE_BASE_URL: str
    ARC_CHAIN: str
    WALLET_ADDRESS: str
    NANO_FEE_USDC: float
    SANDBOX_MODE: bool = False
    class Config:
        env_file = ".env"

settings = Settings()