import os
from dotenv import load_dotenv

load_dotenv()

TFL_API_KEY = os.getenv("TFL_API_KEY")
TFL_BASE_URL = os.getenv("TFL_BASE_URL", "https://api.tfl.gov.uk")

if not TFL_API_KEY:
    raise ValueError("TFL_API_KEY is not set. Please set it in your .env file.")
