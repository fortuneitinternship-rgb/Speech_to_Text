import speech_recognition as sr


class SpeechToText:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        # Speech recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def listen(self):

        with sr.Microphone() as source:

            print("Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = self.recognizer.listen(source)

        return audio

    def transcribe(self, audio):

        try:

            text = self.recognizer.recognize_google(
                audio
            )

            if text and text.strip():

                return text.strip()

            return None

        except sr.UnknownValueError:

            print(
                "⚠️ Could not understand the audio."
            )

            return None

        except sr.RequestError as error:

            print(
                f"⚠️ Speech recognition service error: {error}"
            )

            return None

        except Exception as error:

            print(
                f"⚠️ Unexpected speech recognition error: {error}"
            )

            return None


if __name__ == "__main__":

    stt = SpeechToText()

    audio = stt.listen()

    text = stt.transcribe(audio)

    print("\nVOXINTEL Transcript:")

    if text:

        print(text)

    else:

        print("No valid transcript generated.")