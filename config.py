import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
