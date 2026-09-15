from langdetect import detect, LangDetectException


def detect_language(text):
    try:
        if not text or not text.strip():
            return "Unknown"

        language_code = detect(text)
        return language_code

    except LangDetectException:
        return "Unknown"


if __name__ == "__main__":
    text = input("Enter text: ")

    language_code = detect_language(text)

    print("\nOriginal Text:", text)
    print("Detected Language:", language_code)