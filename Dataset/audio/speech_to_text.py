import speech_recognition as sr

recognizer = sr.Recognizer()

print("Starting Speech-to-Text...")

try:
    with sr.Microphone() as source:
        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source)

        print("Speak now...")
        audio = recognizer.listen(source)

        print("Processing speech...")

        text = recognizer.recognize_google(audio)

        print("\nRecognized Text:")
        print(text)

except sr.WaitTimeoutError:
    print("No speech detected.")

except sr.UnknownValueError:
    print("Sorry, could not understand the audio.")

except sr.RequestError as e:
    print(f"Speech recognition service error: {e}")

except OSError as e:
    print(f"Microphone error: {e}")

except Exception as e:
    print(f"Error: {e}")

print("\nTask 06 completed.")