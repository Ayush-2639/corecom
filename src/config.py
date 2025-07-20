import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")

settings = Settings()
