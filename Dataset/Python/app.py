import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Speech Translator",
    page_icon="🌐",
    layout="centered"
)


# ==========================================
# LANGUAGE LIST
# ==========================================

LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Marathi": "mr"
}


# ==========================================
# TITLE
# ==========================================

st.title("🌐 Speech to Text Translator")

st.write(
    "Speak in one language and translate your speech "
    "into another language."
)

st.divider()


# ==========================================
# LANGUAGE SELECTION
# ==========================================

col1, col2 = st.columns(2)

with col1:

    source_language = st.selectbox(
        "🗣️ From",
        list(LANGUAGES.keys())
    )

with col2:

    target_language = st.selectbox(
        "🌐 To",
        list(LANGUAGES.keys()),
        index=1
    )


source_code = LANGUAGES[source_language]
target_code = LANGUAGES[target_language]


st.divider()


# ==========================================
# SPEECH RECOGNITION
# ==========================================

st.subheader("🎤 Speech Input")

if st.button(
    "🎙️ Start Speaking",
    use_container_width=True
):

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            st.info(
                "🎤 Listening... Please speak now."
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=15
            )

        st.info(
            "🔄 Converting speech to text..."
        )

        # Google speech recognition
        text = recognizer.recognize_google(
            audio,
            language=source_code + "-IN"
        )

        st.session_state["recognized_text"] = text

        st.success(
            "Speech recognized successfully!"
        )

    except sr.WaitTimeoutError:

        st.error(
            "No speech detected. Please try again."
        )

    except sr.UnknownValueError:

        st.error(
            "Sorry, I could not understand the speech."
        )

    except sr.RequestError as e:

        st.error(
            f"Speech recognition service error: {e}"
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )


# ==========================================
# RECOGNIZED TEXT
# ==========================================

if "recognized_text" in st.session_state:

    st.subheader("📝 Recognized Text")

    st.text_area(
        "Speech-to-Text Result",
        st.session_state["recognized_text"],
        height=120
    )


# ==========================================
# TRANSLATION
# ==========================================

if "recognized_text" in st.session_state:

    if st.button(
        "🔄 Translate",
        use_container_width=True
    ):

        try:

            translated_text = GoogleTranslator(
                source=source_code,
                target=target_code
            ).translate(
                st.session_state["recognized_text"]
            )

            st.session_state[
                "translated_text"
            ] = translated_text

            st.success(
                "Translation completed!"
            )

        except Exception as e:

            st.error(
                f"Translation error: {e}"
            )


# ==========================================
# TRANSLATED TEXT
# ==========================================

if "translated_text" in st.session_state:

    st.subheader("🌐 Translation")

    st.text_area(
        "Translated Text",
        st.session_state["translated_text"],
        height=120
    )


# ==========================================
# TEXT TO SPEECH
# ==========================================

if "translated_text" in st.session_state:

    if st.button(
        "🔊 Listen to Translation",
        use_container_width=True
    ):

        try:

            translated_text = (
                st.session_state["translated_text"]
            )

            audio_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )

            audio_file.close()

            speech = gTTS(
                text=translated_text,
                lang=target_code
            )

            speech.save(
                audio_file.name
            )

            st.audio(
                audio_file.name,
                format="audio/mp3"
            )

        except Exception as e:

            st.error(
                f"Text-to-speech error: {e}"
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Speech-to-Text Translator | "
    "English • Telugu • Hindi • Tamil • Marathi"
)