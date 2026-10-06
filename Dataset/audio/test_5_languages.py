import speech_recognition as sr

recognizer = sr.Recognizer()

languages = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "Marathi": "mr-IN"
}

print("=== Speech-to-Text: 5 Language Test ===")

for language_name, language_code in languages.items():

    print(f"\nSpeak in {language_name}...")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    print("Processing...")

    try:
        text = recognizer.recognize_google(
            audio,
            language=language_code
        )

        print(f"{language_name}: {text}")

    except sr.UnknownValueError:
        print(f"{language_name}: Could not understand the audio.")

    except sr.RequestError as e:
        print(f"{language_name}: Recognition service error: {e}")

print("\n=== Test Completed ===")