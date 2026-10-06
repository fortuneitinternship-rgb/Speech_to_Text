from openai import OpenAI
from config import OPENAI_API_KEY


class SpeechEngine:

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. "
                "Please add it to the .env file."
            )

        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def transcribe(self, audio_file):

        result = self.client.audio.transcriptions.create(
            model="gpt-transcribe",
            file=audio_file
        )

        return result.text