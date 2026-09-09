import speech_recognition as sr

# Create recognizer
recognizer = sr.Recognizer()

print("==============================")
print("       VOICE TO TEXT")
print("==============================")

try:
    # Connect to microphone
    with sr.Microphone() as source:
        print("\nAdjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening...")
        audio = recognizer.listen(source)

    # Convert voice to text
    print("\nProcessing speech...")

    text = recognizer.recognize_google(audio)

    print("\nYou said:")
    print(f'"{text}"')

    print("\nSpeech recognized successfully.")

except sr.WaitTimeoutError:
    print("\nNo speech detected. Please try again.")

except sr.UnknownValueError:
    print("\nSorry, I could not understand the speech.")

except sr.RequestError:
    print("\nSpeech recognition service is unavailable.")

except Exception as e:
    print(f"\nAn error occurred: {e}")