from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


class LanguageDetector:

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
        "pa": "Punjabi"
    }

    ENGLISH_WORDS = {
        "i", "you", "he", "she", "we", "they",
        "my", "your", "our", "this", "that",
        "is", "am", "are", "was", "were",
        "the", "a", "an", "and", "or", "but",
        "to", "of", "in", "on", "at", "for",
        "with", "from", "have", "has", "had",
        "do", "does", "did",
        "can", "could", "will", "would",
        "should", "please", "me", "him", "her",
        "hello", "hi", "hey", "how", "what",
        "when", "where", "why", "who",
        "meeting", "reminder", "call",
        "project", "data", "science",
        "machine", "learning", "computer",
        "speech", "language", "conversation",
        "intelligence", "tomorrow", "today",
        "hyderabad", "rahul", "working",
        "morning", "afternoon", "evening"
    }

    def detect_language(self, text):

        if not text or not text.strip():
            return "Unknown"

        text_clean = text.strip().lower()

        # -----------------------------------------
        # INDIAN LANGUAGE UNICODE DETECTION
        # -----------------------------------------

        if any("\u0c00" <= char <= "\u0c7f"
               for char in text_clean):
            return "Telugu"

        if any("\u0b80" <= char <= "\u0bff"
               for char in text_clean):
            return "Tamil"

        if any("\u0980" <= char <= "\u09ff"
               for char in text_clean):
            return "Bengali"

        if any("\u0c80" <= char <= "\u0cff"
               for char in text_clean):
            return "Kannada"

        if any("\u0d00" <= char <= "\u0d7f"
               for char in text_clean):
            return "Malayalam"

        if any("\u0a80" <= char <= "\u0aff"
               for char in text_clean):
            return "Gujarati"

        if any("\u0a00" <= char <= "\u0a7f"
               for char in text_clean):
            return "Punjabi"

        # -----------------------------------------
        # ENGLISH DETECTION
        # -----------------------------------------

        words = (
            text_clean
            .replace(",", "")
            .replace(".", "")
            .replace("!", "")
            .replace("?", "")
            .replace(":", "")
            .replace(";", "")
            .split()
        )

        if not words:
            return "Unknown"

        english_matches = sum(
            1 for word in words
            if word in self.ENGLISH_WORDS
        )

        english_ratio = (
            english_matches / len(words)
        )

        # If most words are common English words,
        # classify as English instead of relying on
        # langdetect for short speech transcripts.
        if (
            english_matches >= 2
            and english_ratio >= 0.30
        ):
            return "English"

        # Very short English speech
        if (
            len(words) <= 4
            and english_matches >= 1
        ):
            return "English"

        # -----------------------------------------
        # LANGDETECT FALLBACK
        # -----------------------------------------

        try:

            language_code = detect(text_clean)

            return self.SUPPORTED_LANGUAGES.get(
                language_code,
                f"Other ({language_code})"
            )

        except Exception:
            return "Unknown"


if __name__ == "__main__":

    detector = LanguageDetector()

    test_sentences = [
        "hello",
        "hay hello how r u",
        "we have a meeting tomorrow",
        "please remind me to call Rahul",
        "I am working on a data science project",
        "This is a multilingual conversation"
    ]

    print("VOXINTEL Language Detection Test")
    print("=" * 50)

    for sentence in test_sentences:

        language = detector.detect_language(
            sentence
        )

        print(
            f"{sentence} -> {language}"
        )