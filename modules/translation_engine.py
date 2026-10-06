from deep_translator import GoogleTranslator


SUPPORTED_LANGUAGES = {
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "mr": "Marathi",
    "bn": "Bengali",
    "kn": "Kannada",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "fr": "French",
}


def translate_text(text, target_language):
    """Translate text into the requested target language."""

    if not text or not text.strip():
        return "No text provided"

    target_language = target_language.lower().strip()

    if target_language not in SUPPORTED_LANGUAGES:
        return f"Unsupported language: {target_language}"

    try:
        translator = GoogleTranslator(
            source="auto",
            target=target_language
        )

        result = translator.translate(text)

        if not result:
            return "Translation service returned no result."

        return result

    except Exception as e:
        error_message = str(e).lower()

        if "too many requests" in error_message or "rate limit" in error_message:
            return (
                "Translation service is temporarily rate-limited. "
                "Please wait and try again later."
            )

        return f"Translation Error: {e}"


def get_supported_languages():
    return SUPPORTED_LANGUAGES