import speech_recognition as sr


def detect_microphone():
    print("\nChecking microphone...")

    try:
        microphones = sr.Microphone.list_microphone_names()

        if not microphones:
            print("No microphone detected.")
            return None

        print("\nAvailable microphones:")

        for index, name in enumerate(microphones):
            print(f"{index}: {name}")

        microphone = sr.Microphone()

        print("\nMicrophone detected successfully.")
        return microphone

    except OSError:
        print("Error: Microphone is not available.")
        return None

    except Exception as error:
        print(f"Unexpected error: {error}")
        return None


def capture_voice(microphone):
    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 1.0
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5

    try:
        with microphone as source:
            print("\nAdjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("\nSpeak now...")
            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

            print("\nVoice captured successfully.")
            print("Audio input received.")

            return audio

    except sr.WaitTimeoutError:
        print("\nError: Listening timeout.")
        print("No speech detected within the time limit.")

    except sr.UnknownValueError:
        print("\nError: No speech detected.")
        print("Please speak clearly and try again.")

    except OSError:
        print("\nError: Audio device unavailable.")
        print("Please check your microphone connection.")

    except Exception as error:
        print(f"\nUnexpected error: {error}")

    return None


def main():
    print("=" * 40)
    print("   Voice Translator Microphone Test")
    print("=" * 40)

    microphone = detect_microphone()

    if microphone is None:
        return

    audio = capture_voice(microphone)

    if audio is not None:
        print("\nTask 05 completed successfully.")
    else:
        print("\nTask 05 completed with an error.")


if __name__ == "__main__":
    main()