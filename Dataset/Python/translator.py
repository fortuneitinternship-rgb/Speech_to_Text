from deep_translator import GoogleTranslator


def translate_text(text, target_language):
    try:
        if not text or not text.strip():
            return "No text provided"

        translated_text = GoogleTranslator(
            source="auto",
            target=target_language
        ).translate(text)

        return translated_text

    except Exception as e:
        return f"Translation Error: {e}"


if __name__ == "__main__":
    text = input("Enter text: ")
    target_language = input(
        "Enter target language code (en/hi/te/ta/mr/fr): "
    )

    translated_text = translate_text(text, target_language)

    print("\nOriginal Text:", text)
    print("Target Language:", target_language)
    print("Translated Text:", translated_text)