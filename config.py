import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

APP_NAME = "VOXINTEL"
APP_VERSION = "1.0.0"

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Marathi": "mr",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "French": "fr",
    "Spanish": "es",
}