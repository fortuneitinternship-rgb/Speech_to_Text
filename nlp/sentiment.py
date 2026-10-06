from textblob import TextBlob


class SentimentAnalyzer:

    def analyze(self, text):

        result = TextBlob(
            text
        ).sentiment

        polarity = result.polarity
        subjectivity = result.subjectivity

        if polarity > 0.1:
            sentiment = "Positive"

        elif polarity < -0.1:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity
        }