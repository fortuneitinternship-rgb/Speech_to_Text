import re
from collections import Counter


class AdvancedNLP:

    def __init__(self):
        self.stopwords = {
            "the", "is", "a", "an", "and", "or",
            "to", "of", "in", "on", "for", "with",
            "this", "that", "are", "was", "were",
            "i", "you", "he", "she", "we", "they",
            "it", "my", "your", "our", "from", "at"
        }

    def clean_text(self, text):

        if not text:
            return ""

        text = text.lower()

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def tokenize(self, text):

        cleaned = self.clean_text(text)

        if not cleaned:
            return []

        return cleaned.split()

    def remove_stopwords(self, text):

        words = self.tokenize(text)

        return [
            word
            for word in words
            if word not in self.stopwords
        ]

    def keyword_extraction(self, text, top_n=10):

        words = self.remove_stopwords(text)

        frequency = Counter(words)

        return frequency.most_common(top_n)

    def word_frequency(self, text):

        words = self.tokenize(text)

        return Counter(words)

    def sentence_count(self, text):

        if not text:
            return 0

        sentences = re.findall(
            r"[^.!?]+",
            text
        )

        return len([
            sentence
            for sentence in sentences
            if sentence.strip()
        ])

    def text_summary(self, text):

        words = self.tokenize(text)

        sentences = self.sentence_count(text)

        return {
            "characters": len(text),
            "words": len(words),
            "unique_words": len(set(words)),
            "sentences": sentences,
            "average_word_length": (
                sum(len(word) for word in words)
                / len(words)
                if words
                else 0
            ),
            "top_keywords": self.keyword_extraction(
                text,
                10
            )
        }