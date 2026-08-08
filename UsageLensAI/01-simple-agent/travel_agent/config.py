import os
 
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("GROQ_MODEL")

from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent
    DB_PATH = BASE_DIR / "usagelens.db"

    @classmethod
    def validate(cls):
        return True