import ast
from collections import Counter
from datetime import datetime

from voxintel.database.conversation_database import ConversationDatabase


class ConversationAnalytics:

    def __init__(self):
        self.database = ConversationDatabase()
        self.conversations = self.load_data()

    def load_data(self):

        rows = self.database.get_all_conversations()

        conversations = []

        for row in rows:

            conversation_id = row[0]
            timestamp = row[1]
            transcript = row[2]
            language = row[3]
            speaker = row[4]
            events_data = row[5]

            # Convert stored events string back to Python list
            try:
                events = ast.literal_eval(events_data)
                if not isinstance(events, list):
                    events = []
            except (ValueError, SyntaxError):
                events = []

            conversations.append({
                "id": conversation_id,
                "timestamp": timestamp,
                "text": transcript,
                "language": language,
                "speaker": speaker,
                "events": events
            })

        return conversations

    # ----------------------------------------
    # BASIC STATISTICS
    # ----------------------------------------

    def total_conversations(self):
        return len(self.conversations)

    def total_words(self):

        total = 0

        for conversation in self.conversations:

            text = conversation.get("text", "")

            total += len(text.split())

        return total

    def average_words(self):

        total = self.total_conversations()

        if total == 0:
            return 0

        return round(
            self.total_words() / total,
            2
        )

    # ----------------------------------------
    # SPEAKER ANALYTICS
    # ----------------------------------------

    def get_speakers(self):

        speakers = []

        for conversation in self.conversations:

            speaker = conversation.get("speaker")

            if speaker and speaker not in speakers:
                speakers.append(speaker)

        return speakers

    def speaker_activity(self):

        activity = Counter()

        for conversation in self.conversations:

            speaker = conversation.get("speaker")

            if speaker:
                activity[speaker] += 1

        return activity

    def speaker_percentages(self):

        activity = self.speaker_activity()

        total = sum(activity.values())

        if total == 0:
            return {}

        return {
            speaker: round(
                (count / total) * 100,
                2
            )
            for speaker, count in activity.items()
        }

    # ----------------------------------------
    # LANGUAGE ANALYTICS
    # ----------------------------------------

    def get_languages(self):

        languages = []

        for conversation in self.conversations:

            language = conversation.get("language")

            if language and language not in languages:
                languages.append(language)

        return languages

    def language_distribution(self):

        languages = Counter()

        for conversation in self.conversations:

            language = conversation.get("language")

            if language:
                languages[language] += 1

        return languages

    # ----------------------------------------
    # EVENT ANALYTICS
    # ----------------------------------------

    def event_statistics(self):

        event_types = []

        for conversation in self.conversations:

            events = conversation.get("events", [])

            for event in events:

                if isinstance(event, dict):

                    event_type = event.get("type")

                    if event_type:
                        event_types.append(event_type)

        return Counter(event_types)

    def total_events(self):

        return sum(
            self.event_statistics().values()
        )

    # ----------------------------------------
    # CONVERSATION ANALYTICS
    # ----------------------------------------

    def longest_conversation(self):

        if not self.conversations:
            return None

        longest = max(
            self.conversations,
            key=lambda conversation:
            len(conversation.get("text", "").split())
        )

        return longest

    def conversations_by_date(self):

        dates = Counter()

        for conversation in self.conversations:

            timestamp = conversation.get("timestamp")

            if timestamp:

                try:

                    date = datetime.fromisoformat(
                        timestamp
                    ).date().isoformat()

                    dates[date] += 1

                except ValueError:
                    continue

        return dates

    # ----------------------------------------
    # SUMMARY
    # ----------------------------------------

    def get_summary(self):

        longest = self.longest_conversation()

        return {
            "total_conversations":
                self.total_conversations(),

            "total_words":
                self.total_words(),

            "average_words":
                self.average_words(),

            "number_of_speakers":
                len(self.get_speakers()),

            "speakers":
                self.get_speakers(),

            "languages":
                self.get_languages(),

            "language_distribution":
                dict(self.language_distribution()),

            "event_statistics":
                dict(self.event_statistics()),

            "total_events":
                self.total_events(),

            "speaker_activity":
                dict(self.speaker_activity()),

            "speaker_percentages":
                self.speaker_percentages(),

            "conversations_by_date":
                dict(self.conversations_by_date()),

            "longest_conversation":
                longest
        }

    # ----------------------------------------
    # TERMINAL REPORT
    # ----------------------------------------

    def generate_report(self):

        print("\n" + "=" * 60)
        print("           VOXINTEL ANALYTICS REPORT")
        print("=" * 60)

        print(
            "\nTotal Conversations:",
            self.total_conversations()
        )

        print(
            "Total Words:",
            self.total_words()
        )

        print(
            "Average Words:",
            self.average_words()
        )

        print(
            "Number of Speakers:",
            len(self.get_speakers())
        )

        print(
            "Speakers:",
            ", ".join(self.get_speakers())
        )

        print(
            "\nLanguages:",
            ", ".join(self.get_languages())
        )

        print("\nLanguage Distribution:")

        for language, count in self.language_distribution().items():

            print(
                f"  {language}: {count}"
            )

        print("\nEvent Statistics:")

        events = self.event_statistics()

        if events:

            for event, count in events.items():

                print(
                    f"  {event}: {count}"
                )

        else:

            print("  No events detected.")

        print(
            "\nTotal Events:",
            self.total_events()
        )

        print("\nSpeaker Activity:")

        for speaker, count in self.speaker_activity().items():

            percentage = self.speaker_percentages().get(
                speaker,
                0
            )

            print(
                f"  {speaker}: "
                f"{count} conversation(s) "
                f"({percentage}%)"
            )

        print("\nConversations by Date:")

        for date, count in self.conversations_by_date().items():

            print(
                f"  {date}: {count}"
            )

        longest = self.longest_conversation()

        if longest:

            print("\nLongest Conversation:")

            print(
                "  Speaker:",
                longest.get("speaker")
            )

            print(
                "  Language:",
                longest.get("language")
            )

            print(
                "  Text:",
                longest.get("text")
            )

        print("\n" + "=" * 60)


if __name__ == "__main__":

    analytics = ConversationAnalytics()

    analytics.generate_report()