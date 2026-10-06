import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.speech_engine import SpeechEngine

audio_path = input("Enter audio file path: ").strip()

engine = SpeechEngine()

with open(audio_path, "rb") as audio_file:
    text = engine.transcribe(audio_file)

print("\n===== TRANSCRIPTION =====")
print(text)