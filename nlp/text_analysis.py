import re
from collections import Counter


class TextAnalyzer:

    STOPWORDS = {
        "the", "is", "a", "an", "and", "or",
        "to", "of", "in", "on", "for", "with",
        "this", "that", "are", "was", "were",
        "i", "you", "he", "she", "we", "they"
    }

    def clean_text(self, text):

        return re.sub(
            r"[^a-zA-Z0-9\s]",
            "",
            text.lower()
        )

    def tokenize(self, text):

        return self.clean_text(text).split()

    def keywords(self, text, top_n=10):

        words = [
            word
            for word in self.tokenize(text)
            if word not in self.STOPWORDS
        ]

        return Counter(words).most_common(top_n)

    def statistics(self, text):

        words = self.tokenize(text)

        return {
            "characters": len(text),
            "words": len(words),
            "unique_words": len(set(words)),
            "sentences": len(
                re.findall(
                    r"[.!?]+",
                    text
                )
            )
        }