from voxintel.speech.speech_to_text import SpeechToText
from voxintel.language.language_detection import LanguageDetector
from voxintel.intelligence.speaker_detection import SpeakerDetector
from voxintel.intelligence.event_extraction import EventExtractor
from voxintel.memory.conversation_memory import ConversationMemory
from voxintel.database.conversation_database import ConversationDatabase
from voxintel.knowledge_graph.knowledge_graph import KnowledgeGraph
from voxintel.analytics.conversation_analytics import ConversationAnalytics


class VoxIntelEngine:

    def __init__(self):

        print("\nInitializing VOXINTEL...")

        # Speech
        self.speech_to_text = SpeechToText()

        # Language
        self.language_detector = LanguageDetector()

        # Speaker
        self.speaker_detector = SpeakerDetector()

        # Intelligence
        self.event_extractor = EventExtractor()

        # Memory
        self.memory = ConversationMemory()

        # Database
        self.database = ConversationDatabase()

        # Knowledge Graph
        self.knowledge_graph = KnowledgeGraph()

        # Analytics
        self.analytics = ConversationAnalytics()

        print("VOXINTEL initialized successfully.")


    def process_voice(self):

        print("\n" + "=" * 60)
        print("                    VOXINTEL")
        print("       Multilingual Conversation Intelligence")
        print("=" * 60)

        # --------------------------------------------------
        # 1. LISTEN
        # --------------------------------------------------

        print("\n[1/8] Listening...")

        audio = self.speech_to_text.listen()

        if audio is None:

            print("\nNo audio captured.")
            print("=" * 60)

            return


        # --------------------------------------------------
        # 2. SPEECH TO TEXT
        # --------------------------------------------------

        print("\n[2/8] Converting speech to text...")

        text = self.speech_to_text.transcribe(audio)

        if not text:

            print("\nNo speech detected.")
            print("Conversation was not saved.")
            print("\n" + "=" * 60)

            return

        print("\nTranscript:")
        print(text)


        # --------------------------------------------------
        # 3. LANGUAGE DETECTION
        # --------------------------------------------------

        print("\n[3/8] Detecting language...")

        language = self.language_detector.detect_language(text)

        print("Detected Language:", language)


        # --------------------------------------------------
        # 4. SPEAKER DETECTION
        # --------------------------------------------------

        print("\n[4/8] Detecting speaker...")

        # Current microphone pipeline uses one voice session.
        # A stable ID allows the SpeakerDetector to assign
        # and remember "Speaker 1".
        speaker_id = "voice_001"

        speaker = self.speaker_detector.assign_speaker(
            speaker_id
        )

        print("Speaker:", speaker)


        # --------------------------------------------------
        # 5. EVENT EXTRACTION
        # --------------------------------------------------

        print("\n[5/8] Extracting events...")

        events = self.event_extractor.extract_events(text)

        if events:

            print("Events detected:")

            for event in events:

                print(" ", event)

        else:

            print("No events detected.")


        # --------------------------------------------------
        # 6. SAVE TO JSON MEMORY
        # --------------------------------------------------

        print("\n[6/8] Saving conversation to memory...")

        self.memory.add_conversation(
            speaker=speaker,
            text=text,
            language=language,
            events=events
        )

        print("Conversation saved to JSON memory.")


        # --------------------------------------------------
        # 7. SAVE TO SQLITE
        # --------------------------------------------------

        print("\n[7/8] Saving conversation to SQLite...")

        self.database.save_conversation(
            transcript=text,
            language=language,
            speaker=speaker,
            events=events
        )

        print("Conversation saved to SQLite database.")


        # --------------------------------------------------
        # 8. KNOWLEDGE GRAPH + ANALYTICS
        # --------------------------------------------------

        print("\n[8/8] Updating Knowledge Graph...")

        # Rebuild the graph from the latest SQLite data.
        # This keeps the graph synchronized with the database.
        self.knowledge_graph.nodes = []
        self.knowledge_graph.relationships = []

        self.knowledge_graph.build_graph()

        print(
            "Knowledge Graph updated."
        )

        print("\nUpdating analytics...")

        # Reload analytics so newly inserted conversations
        # are included in the statistics.
        self.analytics.conversations = (
            self.analytics.load_data()
        )

        print("Analytics updated.")


        # --------------------------------------------------
        # FINAL RESULT
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("              PROCESSING COMPLETE")
        print("=" * 60)

        print("\nVOXINTEL Result:")

        print("Transcript :", text)
        print("Language   :", language)
        print("Speaker    :", speaker)
        print("Events     :", events)

        print("\nDatabase Conversations:",
              self.database.get_conversation_count())

        summary = self.analytics.get_summary()

        print(
            "Total Words:",
            summary["total_words"]
        )

        print(
            "Total Events:",
            summary["total_events"]
        )

        print(
            "Languages:",
            summary["languages"]
        )

        print(
            "Speakers:",
            summary["speakers"]
        )

        print("\nKnowledge Graph:")

        print(
            "Nodes:",
            len(self.knowledge_graph.nodes)
        )

        print(
            "Relationships:",
            len(self.knowledge_graph.relationships)
        )

        print("\n" + "=" * 60)


# ------------------------------------------------------
# MAIN
# ------------------------------------------------------

if __name__ == "__main__":

    engine = VoxIntelEngine()

    engine.process_voice()