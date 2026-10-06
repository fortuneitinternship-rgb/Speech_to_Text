import re


class EventExtractor:

    def extract_events(self, text):

        events = []

        if not text or not text.strip():
            return events

        text_lower = text.lower()

        # MEETING
        if any(word in text_lower for word in [
            "meeting",
            "conference",
            "appointment"
        ]):
            events.append({
                "type": "Meeting",
                "text": text
            })

        # REMINDER
        if any(word in text_lower for word in [
            "remind",
            "remember",
            "reminder"
        ]):
            events.append({
                "type": "Reminder",
                "text": text
            })

        # CALL
        if any(word in text_lower for word in [
            "call",
            "phone",
            "telephone"
        ]):
            events.append({
                "type": "Call",
                "text": text
            })

        # TASK
        if any(word in text_lower for word in [
            "todo",
            "to-do",
            "task",
            "complete",
            "finish",
            "submit",
            "prepare"
        ]):
            events.append({
                "type": "Task",
                "text": text
            })

        # QUESTION
        question_words = [
            "what",
            "why",
            "when",
            "where",
            "who",
            "how",
            "can you",
            "could you",
            "will you"
        ]

        if (
            "?" in text
            or any(
                text_lower.startswith(word)
                for word in question_words
            )
        ):
            events.append({
                "type": "Question",
                "text": text
            })

        # TIME
        time_match = re.search(
            r'\b\d{1,2}(?::\d{2})?\s*(?:a\.?\s*m\.?|p\.?\s*m\.?|am|pm)\b',
            text_lower
        )

        if time_match:
            events.append({
                "type": "Time",
                "value": time_match.group()
            })

        # DATE
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'
        ]

        for pattern in date_patterns:

            date_match = re.search(pattern, text)

            if date_match:
                events.append({
                    "type": "Date",
                    "value": date_match.group()
                })
                break

        # PHONE
        phone_match = re.search(
            r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)',
            text
        )

        if phone_match:
            events.append({
                "type": "Phone",
                "value": phone_match.group()
            })

        # MONEY
        money_match = re.search(
            r'(?:₹|rs\.?|inr)\s?[\d,]+(?:\.\d{1,2})?',
            text_lower
        )

        if money_match:
            events.append({
                "type": "Amount",
                "value": money_match.group()
            })

        # LOCATION
        locations = [
            "hyderabad",
            "visakhapatnam",
            "vizag",
            "bangalore",
            "bengaluru",
            "chennai",
            "mumbai",
            "delhi",
            "pune"
        ]

        for location in locations:

            if re.search(
                r'\b' + re.escape(location) + r'\b',
                text_lower
            ):
                events.append({
                    "type": "Location",
                    "value": location.title()
                })

        return events


if __name__ == "__main__":

    extractor = EventExtractor()

    test_sentences = [
        "We have a meeting at 10 AM.",
        "Please remind me to call Rahul.",
        "I need to complete this task.",
        "Can you send the report?",
        "Our meeting is on 25/09/2026.",
        "Call me at 9876543210.",
        "The payment amount is ₹5000.",
        "We have a meeting in Hyderabad at 3:00 p.m."
    ]

    print("VOXINTEL Event Extraction Test")
    print("=" * 60)

    for sentence in test_sentences:

        print("\nText:", sentence)

        events = extractor.extract_events(sentence)

        print("Events:")

        if events:

            for event in events:
                print(" ", event)

        else:
            print("  No events detected.")