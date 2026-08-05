import speech_recognition as sr
from deep_translator import GoogleTranslator

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)

    translated = GoogleTranslator(source='auto', target='te').translate(text)
    print("Translated Text:", translated)

except Exception as e:
    print("Error:", e)