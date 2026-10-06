import json
import os

import streamlit as st

from config import APP_NAME, APP_VERSION

from voxintel.speech.speech_to_text import SpeechToText
from voxintel.language.language_detection import LanguageDetector
from voxintel.intelligence.speaker_detection import SpeakerDetector
from voxintel.intelligence.event_extraction import EventExtractor
from voxintel.memory.conversation_memory import ConversationMemory

from modules.translation_engine import (
    translate_text,
    get_supported_languages
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VOXINTEL",
    page_icon="🎙️",
    layout="wide"
)


# ============================================================
# LOAD VOXINTEL COMPONENTS
# ============================================================

speech_to_text = SpeechToText()
language_detector = LanguageDetector()
speaker_detector = SpeakerDetector()
event_extractor = EventExtractor()
memory = ConversationMemory()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_conversations():

    file_path = "conversation_memory.json"

    if not os.path.exists(file_path):
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception:
        return []


def calculate_statistics(conversations):

    total_conversations = len(conversations)
    total_words = 0

    languages = {}
    speakers = {}
    events = {}

    for conversation in conversations:

        text = conversation.get(
            "text",
            ""
        )

        total_words += len(text.split())

        language = conversation.get(
            "language",
            "Unknown"
        )

        languages[language] = (
            languages.get(language, 0) + 1
        )

        speaker = conversation.get(
            "speaker",
            "Unknown"
        )

        speakers[speaker] = (
            speakers.get(speaker, 0) + 1
        )

        for event in conversation.get(
            "events",
            []
        ):

            event_type = event.get(
                "type",
                "Unknown"
            )

            events[event_type] = (
                events.get(event_type, 0) + 1
            )

    average_words = (
        total_words / total_conversations
        if total_conversations > 0
        else 0
    )

    return (
        total_conversations,
        total_words,
        average_words,
        languages,
        speakers,
        events
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎙️ VOXINTEL")

st.sidebar.caption(
    f"Version {APP_VERSION}"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🎙️ Speech-to-Text",
        "🌐 Translation",
        "🧠 Conversation Memory",
        "📊 Analytics",
        "📌 Event Intelligence",
        "🕸️ Knowledge Graph"
    ]
)


# ============================================================
# LOAD DATA
# ============================================================

conversations = load_conversations()

(
    total_conversations,
    total_words,
    average_words,
    languages,
    speakers,
    events
) = calculate_statistics(
    conversations
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("🎙️ VOXINTEL")

    st.subheader(
        "Multilingual Conversation Intelligence & Memory Engine"
    )

    st.markdown(
        """
        VOXINTEL transforms speech into structured
        conversation intelligence.

        **Voice → Speech → Language → Speaker → Events → Memory → Analytics**
        """
    )

    st.divider()

    st.header("📊 System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Conversations",
            total_conversations
        )

    with col2:
        st.metric(
            "Total Words",
            total_words
        )

    with col3:
        st.metric(
            "Languages",
            len(languages)
        )

    with col4:
        st.metric(
            "Events",
            sum(events.values())
        )

    st.divider()

    st.header("🚀 Core Pipeline")

    pipeline = [
        "🎙️ Speech Recognition",
        "📝 Speech-to-Text",
        "🌐 Language Detection",
        "👤 Speaker Identification",
        "📌 Event Extraction",
        "🧠 Conversation Memory",
        "📊 Analytics"
    ]

    for step_number, step in enumerate(
        pipeline,
        start=1
    ):

        st.write(
            f"**{step_number}.** {step}"
        )

    st.divider()

    st.header("🌐 Supported Languages")

    language_names = [
        "English",
        "Telugu",
        "Hindi",
        "Tamil",
        "Marathi",
        "Bengali",
        "Kannada",
        "Malayalam",
        "Gujarati",
        "Punjabi",
        "French"
    ]

    st.write(
        " • ".join(language_names)
    )


# ============================================================
# SPEECH-TO-TEXT
# ============================================================

elif page == "🎙️ Speech-to-Text":

    st.title("🎙️ Live Speech-to-Text")

    st.write(
        "Speak into your microphone and VOXINTEL "
        "will convert your speech into structured intelligence."
    )

    if st.button(
        "🎤 Start Listening",
        type="primary"
    ):

        with st.spinner(
            "Listening for speech..."
        ):

            try:

                audio = speech_to_text.listen()

                transcript = speech_to_text.transcribe(
                    audio
                )

                if transcript:

                    st.subheader("📝 Transcript")

                    st.success(transcript)

                    # ----------------------------------------
                    # Language Detection
                    # ----------------------------------------

                    try:

                        language = (
                            language_detector.detect_language(
                                transcript
                            )
                        )

                    except Exception:

                        language = "Unknown"

                    st.subheader(
                        "🌐 Detected Language"
                    )

                    st.info(language)

                    # ----------------------------------------
                    # Speaker Assignment
                    # ----------------------------------------

                    try:

                        speaker = (
                            speaker_detector.assign_speaker(
                                "voice_001"
                            )
                        )

                    except Exception:

                        speaker = "Speaker 1"

                    st.subheader("👤 Speaker")

                    st.info(speaker)

                    # ----------------------------------------
                    # Event Extraction
                    # ----------------------------------------

                    try:

                        detected_events = (
                            event_extractor.extract_events(
                                transcript
                            )
                        )

                    except Exception:

                        detected_events = []

                    st.subheader("📌 Events")

                    if detected_events:

                        for event in detected_events:

                            st.write(
                                f"• {event}"
                            )

                    else:

                        st.write(
                            "No events detected."
                        )

                    # ----------------------------------------
                    # Save Conversation
                    # ----------------------------------------

                    try:

                        memory.add_conversation(
                            speaker=speaker,
                            text=transcript,
                            language=language,
                            events=detected_events
                        )

                        st.success(
                            "🧠 Conversation saved to memory."
                        )

                    except Exception as error:

                        st.warning(
                            f"Could not save conversation: {error}"
                        )

                else:

                    st.warning(
                        "No speech was detected."
                    )

            except Exception as error:

                st.error(
                    f"Speech recognition error: {error}"
                )


# ============================================================
# TRANSLATION
# ============================================================

elif page == "🌐 Translation":

    st.title("🌐 VOXINTEL Translation")

    st.write(
        "Translate conversation text into another language."
    )

    supported_languages = (
        get_supported_languages()
    )

    language_codes = list(
        supported_languages.keys()
    )

    language_labels = [
        f"{code.upper()} - {supported_languages[code]}"
        for code in language_codes
    ]

    text_input = st.text_area(
        "📝 Enter text to translate",
        height=180,
        placeholder="Enter your conversation text here..."
    )

    col1, col2 = st.columns(2)

    with col1:

        source_display = st.selectbox(
            "Source Language",
            ["AUTO - Detect automatically"]
            + language_labels
        )

    with col2:

        target_display = st.selectbox(
            "Target Language",
            language_labels,
            index=(
                language_codes.index("te")
                if "te" in language_codes
                else 0
            )
        )

    target_code = target_display.split(
        " - "
    )[0].lower()

    st.divider()

    if st.button(
        "🌐 Translate",
        type="primary"
    ):

        if not text_input.strip():

            st.warning(
                "Please enter some text first."
            )

        else:

            with st.spinner(
                "Translating..."
            ):

                result = translate_text(
                    text_input,
                    target_code
                )

            st.subheader(
                "📖 Original Text"
            )

            st.write(text_input)

            st.subheader(
                "🔄 Translated Text"
            )

            if result.startswith(
                "Translation service is temporarily"
            ):

                st.warning(result)

            elif result.startswith(
                "Translation Error"
            ):

                st.error(result)

            else:

                st.success(result)

    st.divider()

    st.subheader(
        "🌍 Supported Languages"
    )

    language_columns = st.columns(3)

    for index, code in enumerate(
        language_codes
    ):

        with language_columns[
            index % 3
        ]:

            st.write(
                f"**{code.upper()}** — "
                f"{supported_languages[code]}"
            )


# ============================================================
# CONVERSATION MEMORY
# ============================================================

elif page == "🧠 Conversation Memory":

    st.title("🧠 Conversation Memory")

    st.write(
        "All conversations stored by VOXINTEL."
    )

    if not conversations:

        st.info(
            "No conversations stored yet."
        )

    else:

        st.metric(
            "Stored Conversations",
            len(conversations)
        )

        st.divider()

        for index, conversation in enumerate(
            reversed(conversations),
            start=1
        ):

            with st.expander(
                f"Conversation {index}"
            ):

                st.write(
                    "**Timestamp:**",
                    conversation.get(
                        "timestamp",
                        "Unknown"
                    )
                )

                st.write(
                    "**Speaker:**",
                    conversation.get(
                        "speaker",
                        "Unknown"
                    )
                )

                st.write(
                    "**Language:**",
                    conversation.get(
                        "language",
                        "Unknown"
                    )
                )

                st.write(
                    "**Text:**",
                    conversation.get(
                        "text",
                        ""
                    )
                )

                conversation_events = (
                    conversation.get(
                        "events",
                        []
                    )
                )

                if conversation_events:

                    st.write(
                        "**Events:**"
                    )

                    for event in conversation_events:

                        st.write(
                            f"• {event}"
                        )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.title("📊 Conversation Analytics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Conversations",
            total_conversations
        )

    with col2:

        st.metric(
            "Total Words",
            total_words
        )

    with col3:

        st.metric(
            "Average Words",
            f"{average_words:.1f}"
        )

    with col4:

        st.metric(
            "Total Events",
            sum(events.values())
        )

    st.divider()

    st.subheader(
        "🌐 Language Distribution"
    )

    if languages:

        for language, count in languages.items():

            st.write(
                f"**{language}:** {count}"
            )

    else:

        st.info(
            "No language data available."
        )

    st.divider()

    st.subheader(
        "👤 Speaker Activity"
    )

    if speakers:

        for speaker, count in speakers.items():

            st.write(
                f"**{speaker}:** {count} conversations"
            )

    else:

        st.info(
            "No speaker data available."
        )

    st.divider()

    st.subheader(
        "📌 Event Statistics"
    )

    if events:

        for event_type, count in events.items():

            st.write(
                f"**{event_type}:** {count}"
            )

    else:

        st.info(
            "No events available."
        )


# ============================================================
# EVENT INTELLIGENCE
# ============================================================

elif page == "📌 Event Intelligence":

    st.title("📌 Event Intelligence")

    st.write(
        "Events extracted from stored conversations."
    )

    if not events:

        st.info(
            "No events have been detected yet."
        )

    else:

        for event_type, count in events.items():

            st.metric(
                event_type,
                count
            )

        st.divider()

        st.subheader(
            "Conversation Event Details"
        )

        for conversation in conversations:

            conversation_events = (
                conversation.get(
                    "events",
                    []
                )
            )

            if conversation_events:

                st.write(
                    f"**{conversation.get('text', '')}**"
                )

                for event in conversation_events:

                    st.write(
                        f"• {event}"
                    )


# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

elif page == "🕸️ Knowledge Graph":

    st.title("🕸️ Knowledge Graph")

    st.info(
        "The Knowledge Graph will connect people, "
        "locations, meetings, calls, projects and "
        "other entities extracted from conversations."
    )

    st.subheader(
        "Planned Entities"
    )

    entities = [
        "👤 People",
        "📍 Locations",
        "📅 Dates",
        "⏰ Times",
        "📞 Calls",
        "🤝 Meetings",
        "📌 Tasks",
        "🔔 Reminders",
        "💰 Amounts",
        "🌐 Languages"
    ]

    for entity in entities:

        st.write(
            f"• {entity}"
        )

    st.divider()

    st.subheader(
        "Current Event Connections"
    )

    if events:

        for event_type, count in events.items():

            st.write(
                f"**{event_type}** → {count} occurrence(s)"
            )

    else:

        st.info(
            "No event connections available yet."
        )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "VOXINTEL – Multilingual Conversation "
    "Intelligence & Memory Engine"
)

