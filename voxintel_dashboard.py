import streamlit as st
import sqlite3
import pandas as pd
import io
import ast

from voxintel.analytics.conversation_analytics import ConversationAnalytics
from voxintel.knowledge_graph.knowledge_graph import KnowledgeGraph
from voxintel.intelligence.speaker_detection import SpeakerDetector
from voxintel.language.language_detection import LanguageDetector
from voxintel.intelligence.event_extraction import EventExtractor
from voxintel.memory.conversation_memory import ConversationMemory
from voxintel.database.conversation_database import ConversationDatabase

from data_science.eda import EDAAnalyzer
from data_science.statistics import StatisticsAnalyzer
from data_science.visualization import VisualizationEngine
from data_science.ml_models import MLAnalyzer
from nlp.text_analysis import TextAnalyzer
from nlp.sentiment import SentimentAnalyzer
from nlp.advanced_nlp import AdvancedNLP
from business.business_analytics import BusinessAnalytics
from business.customer_segmentation import CustomerSegmentation
from business.fraud_detection import FraudDetector
from business.sales_forecasting import SalesForecaster


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VOXINTEL",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "voxintel.db"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    font-size: 18px;
    opacity: 0.70;
    margin-bottom: 25px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
}

div[data-testid="stMetric"] {
    border-radius: 12px;
    padding: 15px;
    border: 1px solid rgba(128,128,128,0.20);
}

div[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: 700;
}

div[data-testid="stMetricLabel"] {
    font-size: 15px;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.20);
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# DATABASE
# ============================================================

def load_conversations():
    try:
        conn = sqlite3.connect(DB_PATH)
        query = """
        SELECT id, timestamp, transcript, language, speaker, events
        FROM conversations
        ORDER BY id DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame(
            columns=[
                "id", "timestamp", "transcript",
                "language", "speaker", "events"
            ]
        )


def parse_events(value):
    if not value:
        return []
    try:
        events = ast.literal_eval(str(value))
        return events if isinstance(events, list) else []
    except Exception:
        return []


def event_counts(df):
    counter = {}
    if df.empty:
        return counter

    for value in df["events"]:
        for event in parse_events(value):
            if isinstance(event, dict):
                event_type = event.get("type", "Unknown")
            else:
                event_type = str(event)
            counter[event_type] = counter.get(event_type, 0) + 1

    return counter


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

df = load_conversations()

analytics = ConversationAnalytics()
graph = KnowledgeGraph()
speaker_detector = SpeakerDetector()
language_detector = LanguageDetector()
event_extractor = EventExtractor()
memory = ConversationMemory()
database = ConversationDatabase()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎙️ VOXINTEL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Multilingual Conversation & Customer Intelligence Platform'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎙️ VOXINTEL")
st.sidebar.markdown("### AI + Data Science Platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "🎙️ Speech-to-Text",
        "🧠 Conversation Intelligence",
        "😊 Sentiment & NLP",
        "👥 Customer Segmentation",
        "🚨 Fraud Detection",
        "📈 Sales Forecasting",
        "📊 Business Analytics",
        "🔬 EDA & Statistics",
        "🤖 Machine Learning",
        "🕸️ Knowledge Graph",
        "💾 Conversation Database",
        "📈 Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("🟢 System Online")
st.sidebar.metric("Conversations", len(df))

total_words_sidebar = (
    sum(len(str(x).split()) for x in df["transcript"])
    if not df.empty else 0
)
st.sidebar.metric("Total Words", total_words_sidebar)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Speech → NLP → Intelligence → Data Science → Business Insights"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.header("📊 VOXINTEL Dashboard")

    total_conversations = len(df)

    if not df.empty:
        total_words = sum(
            len(str(text).split())
            for text in df["transcript"]
        )
        average_words = (
            total_words / total_conversations
            if total_conversations else 0
        )
        total_speakers = df["speaker"].dropna().nunique()
        total_languages = df["language"].dropna().nunique()
        total_events = sum(event_counts(df).values())
    else:
        total_words = 0
        average_words = 0
        total_speakers = 0
        total_languages = 0
        total_events = 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💬 Conversations", total_conversations)
    col2.metric("📝 Total Words", total_words)
    col3.metric("👤 Speakers", total_speakers)
    col4.metric("🌐 Languages", total_languages)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Average Words", round(average_words, 2))
    col2.metric("🧠 Total Events", total_events)
    col3.metric("💾 Database Rows", len(df))
    col4.metric("🟢 System", "Online")

    st.markdown("---")

    if not df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🌐 Language Distribution")
            st.bar_chart(
                df["language"].fillna("Unknown").value_counts()
            )

        with col2:
            st.subheader("👤 Speaker Activity")
            st.bar_chart(
                df["speaker"].fillna("Unknown").value_counts()
            )

        st.subheader("🧠 Event Statistics")
        counts = event_counts(df)
        if counts:
            event_df = pd.DataFrame(
                list(counts.items()),
                columns=["Event", "Count"]
            )
            st.bar_chart(event_df.set_index("Event"))
        else:
            st.info("No events detected yet.")

        st.subheader("🕒 Recent Conversations")
        recent = df.head(10)[
            ["id", "timestamp", "transcript", "language", "speaker"]
        ]
        st.dataframe(recent, width="stretch", hide_index=True)

    else:
        st.info(
            "No conversations stored yet. Use Speech-to-Text "
            "to create your first conversation."
        )

    st.markdown("---")
    st.subheader("🚀 Data Science Platform")

    cards = [
        ("😊 NLP", "Text analysis, keywords and sentiment"),
        ("👥 Segmentation", "RFM customer intelligence"),
        ("🚨 Fraud", "Machine-learning risk detection"),
        ("📈 Forecasting", "Sales trend and prediction"),
        ("🔬 EDA", "Data quality and statistics"),
        ("🤖 ML", "Classification and regression")
    ]

    cols = st.columns(3)
    for i, (title, description) in enumerate(cards):
        with cols[i % 3]:
            st.info(f"**{title}**\n\n{description}")


# ============================================================
# SPEECH TO TEXT
# ============================================================

elif page == "🎙️ Speech-to-Text":

    st.header("🎙️ Speech-to-Text")
    st.write("Record your voice and convert it into conversation intelligence.")

    try:
        import speech_recognition as sr
        from audiorecorder import audiorecorder

        audio = audiorecorder(
            "▶️ Start Recording",
            "⏹️ Stop Recording"
        )

        if len(audio) > 0:
            st.success("✅ Audio recorded successfully!")

            audio_preview = io.BytesIO()
            audio.export(audio_preview, format="wav")
            audio_preview.seek(0)
            st.audio(audio_preview, format="audio/wav")

            if st.button(
                "🔊 Convert Speech to Text",
                type="primary"
            ):
                recognizer = sr.Recognizer()
                wav_buffer = io.BytesIO()
                audio.export(wav_buffer, format="wav")
                wav_buffer.seek(0)

                try:
                    with sr.AudioFile(wav_buffer) as source:
                        audio_data = recognizer.record(source)

                    text_result = recognizer.recognize_google(
                        audio_data
                    ).strip()

                    if text_result:
                        st.success("✅ Speech recognized successfully!")
                        st.subheader("📄 Transcript")
                        st.text_area(
                            "Recognized Text",
                            text_result,
                            height=150
                        )

                        detected_language = (
                            language_detector.detect_language(
                                text_result
                            )
                        )
                        detected_events = (
                            event_extractor.extract_events(
                                text_result
                            )
                        )

                        col1, col2 = st.columns(2)
                        col1.metric(
                            "🌐 Language",
                            detected_language
                        )
                        col2.metric(
                            "🧠 Events",
                            len(detected_events)
                        )

                        if detected_events:
                            st.subheader("🧠 Detected Events")
                            for event in detected_events:
                                st.json(event)

                        if st.button("💾 Save Conversation"):
                            speaker = speaker_detector.assign_speaker(
                                "voice_001"
                            )

                            memory.add_conversation(
                                speaker=speaker,
                                text=text_result,
                                language=detected_language,
                                events=detected_events
                            )

                            database.save_conversation(
                                transcript=text_result,
                                language=detected_language,
                                speaker=speaker,
                                events=detected_events
                            )

                            st.success(
                                "✅ Conversation saved successfully!"
                            )
                            st.rerun()

                except sr.UnknownValueError:
                    st.error("❌ Speech could not be understood.")
                except sr.RequestError as e:
                    st.error(f"❌ Speech recognition service error: {e}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    except ImportError:
        st.error("Speech-to-Text dependencies are missing.")
        st.code(
            "pip install SpeechRecognition audio-recorder-streamlit"
        )


# ============================================================
# CONVERSATION INTELLIGENCE
# ============================================================

elif page == "🧠 Conversation Intelligence":

    st.header("🧠 Conversation Intelligence")
    st.write(
        "Analyze multilingual conversations using language detection, "
        "speaker identification and event extraction."
    )

    text_input = st.text_area(
        "Enter conversation text",
        height=180,
        placeholder=(
            "Example: We have a meeting tomorrow at 10 AM "
            "in Hyderabad. Please remind me to call Rahul."
        )
    )

    if st.button(
        "🔍 Analyze Conversation",
        type="primary"
    ):
        if not text_input.strip():
            st.warning("Please enter some text.")
        else:
            language = language_detector.detect_language(text_input)
            speaker = speaker_detector.assign_speaker("voice_001")
            events = event_extractor.extract_events(text_input)

            col1, col2, col3 = st.columns(3)
            col1.metric("🌐 Language", language)
            col2.metric("👤 Speaker", speaker)
            col3.metric("🧠 Events", len(events))

            st.subheader("📄 Transcript")
            st.write(text_input)

            st.subheader("🧠 Extracted Events")
            if events:
                for event in events:
                    st.json(event)
            else:
                st.info("No events detected.")


# ============================================================
# SENTIMENT & NLP
# ============================================================

elif page == "😊 Sentiment & NLP":

    st.header("😊 Sentiment & NLP")
    st.write(
        "Analyze conversation text using NLP, sentiment analysis, "
        "keywords and text statistics."
    )

    text = st.text_area(
        "Enter text for NLP analysis",
        height=180,
        placeholder="Example: The customer is very happy with our service."
    )

    if st.button("🧠 Run NLP Analysis", type="primary"):

        if not text.strip():
            st.warning("Please enter text.")
        else:
            analyzer = TextAnalyzer()
            sentiment = SentimentAnalyzer()
            advanced = AdvancedNLP()

            result = sentiment.analyze(text)
            stats = analyzer.statistics(text)
            keywords = analyzer.keywords(text, 10)
            summary = advanced.text_summary(text)

            st.subheader("😊 Sentiment")
            c1, c2, c3 = st.columns(3)
            c1.metric("Sentiment", result["sentiment"])
            c2.metric("Polarity", round(result["polarity"], 3))
            c3.metric("Subjectivity", round(result["subjectivity"], 3))

            st.subheader("📝 Text Statistics")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Characters", stats["characters"])
            c2.metric("Words", stats["words"])
            c3.metric("Unique Words", stats["unique_words"])
            c4.metric("Sentences", stats["sentences"])

            st.subheader("🔑 Top Keywords")
            keyword_df = pd.DataFrame(
                keywords,
                columns=["Keyword", "Frequency"]
            )
            st.dataframe(
                keyword_df,
                width="stretch",
                hide_index=True
            )

            st.subheader("🧠 Advanced NLP Summary")
            st.json(summary)


# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

elif page == "👥 Customer Segmentation":

    st.header("👥 Customer Segmentation")
    st.write(
        "Segment customers using Recency, Frequency and Monetary (RFM) analysis."
    )

    uploaded = st.file_uploader(
        "Upload customer transaction CSV",
        type=["csv"],
        key="segmentation_csv"
    )

    if uploaded:
        data = pd.read_csv(uploaded)
        st.write("Dataset preview")
        st.dataframe(data.head(), width="stretch")

        columns = data.columns.tolist()

        if len(columns) >= 3:
            c1, c2, c3 = st.columns(3)

            customer_col = c1.selectbox(
                "Customer column",
                columns,
                key="seg_customer"
            )
            date_col = c2.selectbox(
                "Date column",
                columns,
                key="seg_date"
            )
            value_col = c3.selectbox(
                "Value / Sales column",
                columns,
                key="seg_value"
            )

            clusters = st.slider(
                "Number of clusters",
                min_value=2,
                max_value=6,
                value=4
            )

            if st.button(
                "👥 Run Customer Segmentation",
                type="primary"
            ):
                try:
                    segmenter = CustomerSegmentation(data)
                    rfm = segmenter.run(
                        customer_col,
                        date_col,
                        value_col,
                        clusters
                    )

                    st.subheader("📊 Customer Segments")
                    st.dataframe(
                        rfm,
                        width="stretch",
                        hide_index=True
                    )

                    summary = segmenter.segment_summary(rfm)

                    st.subheader("📈 Segment Summary")
                    st.dataframe(
                        summary,
                        width="stretch",
                        hide_index=True
                    )

                    if not summary.empty:
                        st.bar_chart(
                            summary.set_index("Segment")["Customers"]
                        )

                except Exception as e:
                    st.error(f"Segmentation error: {e}")

    else:
        st.info(
            "Upload a CSV containing customer, date and transaction value "
            "columns to run RFM segmentation."
        )


# ============================================================
# FRAUD DETECTION
# ============================================================

elif page == "🚨 Fraud Detection":

    st.header("🚨 Fraud Detection")
    st.write(
        "Train a Random Forest model to identify potentially fraudulent transactions."
    )

    uploaded = st.file_uploader(
        "Upload fraud transaction CSV",
        type=["csv"],
        key="fraud_csv"
    )

    if uploaded:
        data = pd.read_csv(uploaded)

        st.dataframe(
            data.head(),
            width="stretch"
        )

        target = st.selectbox(
            "Select fraud target column",
            data.columns.tolist(),
            key="fraud_target"
        )

        if st.button(
            "🚨 Train Fraud Model",
            type="primary"
        ):
            try:
                detector = FraudDetector(data)
                metrics = detector.train_model(target)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Accuracy", f"{metrics['accuracy']:.2%}")
                c2.metric("Precision", f"{metrics['precision']:.2%}")
                c3.metric("Recall", f"{metrics['recall']:.2%}")
                c4.metric("F1 Score", f"{metrics['f1']:.2%}")

                st.subheader("🔍 Feature Importance")
                importance = detector.feature_importance()
                st.dataframe(
                    importance,
                    width="stretch",
                    hide_index=True
                )
                st.bar_chart(
                    importance.set_index("Feature")["Importance"]
                )

                st.session_state["fraud_detector"] = detector

            except Exception as e:
                st.error(f"Fraud model error: {e}")

    else:
        st.info(
            "Upload a labelled transaction CSV to train the fraud detection model."
        )


# ============================================================
# SALES FORECASTING
# ============================================================

elif page == "📈 Sales Forecasting":

    st.header("📈 Sales Forecasting")
    st.write(
        "Analyze historical sales trends, moving averages and future sales."
    )

    uploaded = st.file_uploader(
        "Upload sales CSV",
        type=["csv"],
        key="forecast_csv"
    )

    if uploaded:
        data = pd.read_csv(uploaded)
        st.dataframe(data.head(), width="stretch")

        columns = data.columns.tolist()

        if len(columns) >= 2:
            c1, c2 = st.columns(2)

            date_col = c1.selectbox(
                "Date column",
                columns,
                key="forecast_date"
            )

            sales_col = c2.selectbox(
                "Sales column",
                columns,
                key="forecast_sales"
            )

            periods = st.slider(
                "Forecast days",
                min_value=1,
                max_value=30,
                value=7
            )

            if st.button(
                "📈 Generate Forecast",
                type="primary"
            ):
                try:
                    forecaster = SalesForecaster(data)

                    prepared = forecaster.prepare_data(
                        date_col,
                        sales_col
                    )

                    trend = forecaster.trend(
                        date_col,
                        sales_col
                    )

                    moving = forecaster.moving_average(
                        date_col,
                        sales_col,
                        3
                    )

                    forecast = forecaster.forecast(
                        date_col,
                        sales_col,
                        periods
                    )

                    summary = forecaster.summary(
                        date_col,
                        sales_col,
                        periods
                    )

                    c1, c2, c3 = st.columns(3)
                    c1.metric(
                        "Historical Sales",
                        f"{summary['historical_sales']:.2f}"
                    )
                    c2.metric(
                        "Forecast Sales",
                        f"{summary['forecast_sales']:.2f}"
                    )
                    c3.metric(
                        "Trend",
                        trend["direction"]
                    )

                    st.subheader("📊 Historical Sales")
                    historical_chart = prepared.set_index(date_col)[
                        [sales_col]
                    ]
                    st.line_chart(historical_chart)

                    st.subheader("📉 Moving Average")
                    moving_chart = moving.set_index(date_col)[
                        [sales_col, "Moving Average"]
                    ]
                    st.line_chart(moving_chart)

                    st.subheader("🔮 Future Sales Forecast")
                    st.dataframe(
                        forecast,
                        width="stretch",
                        hide_index=True
                    )

                    st.line_chart(
                        forecast.set_index("Date")[
                            ["Forecast Sales"]
                        ]
                    )

                    st.success(
                        f"Forecast completed for the next {periods} days."
                    )

                except Exception as e:
                    st.error(f"Forecasting error: {e}")

    else:
        st.info(
            "Upload a CSV containing a date column and a sales/revenue column."
        )


# ============================================================
# BUSINESS ANALYTICS
# ============================================================

elif page == "📊 Business Analytics":

    st.header("📊 Business Analytics")
    st.write(
        "Generate KPIs, group analysis, customer analysis and business insights."
    )

    uploaded = st.file_uploader(
        "Upload business CSV",
        type=["csv"],
        key="business_csv"
    )

    if uploaded:
        data = pd.read_csv(uploaded)

        st.dataframe(
            data.head(),
            width="stretch"
        )

        numeric_columns = data.select_dtypes(
            include="number"
        ).columns.tolist()

        all_columns = data.columns.tolist()

        if numeric_columns:
            value_col = st.selectbox(
                "Select numeric value column",
                numeric_columns,
                key="business_value"
            )

            if st.button(
                "📊 Analyze Business Data",
                type="primary"
            ):
                try:
                    business = BusinessAnalytics(data)
                    summary = business.summary()
                    kpi = business.calculate_kpi(value_col)
                    insights = business.generate_insights(value_col)

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Rows", summary["rows"])
                    c2.metric("Columns", summary["columns"])
                    c3.metric(
                        "Numeric Columns",
                        summary["total_numeric_columns"]
                    )

                    st.subheader("💰 KPI Analysis")
                    st.json(kpi)

                    st.subheader("💡 Business Insights")
                    for insight in insights:
                        st.info(insight)

                    st.subheader("🚨 Outlier Analysis")
                    outliers = business.detect_outliers(value_col)
                    st.write(
                        f"Outliers detected: **{outliers['count']}**"
                    )
                    st.write(
                        f"Lower bound: **{outliers['lower_bound']:.2f}**"
                    )
                    st.write(
                        f"Upper bound: **{outliers['upper_bound']:.2f}**"
                    )

                    if outliers["count"] > 0:
                        st.dataframe(
                            outliers["outliers"],
                            width="stretch",
                            hide_index=True
                        )

                except Exception as e:
                    st.error(f"Business analytics error: {e}")

        else:
            st.warning("No numeric columns found in this dataset.")

    else:
        st.info("Upload a business dataset CSV to begin analysis.")


# ============================================================
# EDA & STATISTICS
# ============================================================

elif page == "🔬 EDA & Statistics":

    st.header("🔬 EDA & Statistics")
    st.write(
        "Explore data quality, descriptive statistics, correlations and distributions."
    )

    uploaded = st.file_uploader(
        "Upload CSV for EDA",
        type=["csv"],
        key="eda_csv"
    )

    if uploaded:
        data = pd.read_csv(uploaded)

        eda = EDAAnalyzer(data)
        stats = StatisticsAnalyzer(data)

        summary = eda.summary()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", summary["rows"])
        c2.metric("Columns", summary["columns"])
        c3.metric("Missing Values", summary["missing_values"])
        c4.metric("Duplicates", summary["duplicate_rows"])

        st.subheader("👀 Dataset Preview")
        st.dataframe(
            data.head(20),
            width="stretch",
            hide_index=True
        )

        st.subheader("📋 Data Types")
        st.dataframe(
            eda.data_types().rename("Data Type").to_frame(),
            width="stretch"
        )

        st.subheader("📊 Descriptive Statistics")
        st.dataframe(
            stats.numeric_summary(),
            width="stretch"
        )

        st.subheader("🔗 Correlation Matrix")
        correlation = eda.correlation()
        if not correlation.empty:
            st.dataframe(
                correlation,
                width="stretch"
            )
        else:
            st.info("No numeric columns available.")

        numeric_columns = eda.numerical_columns()
        categorical_columns = eda.categorical_columns()

        if numeric_columns:
            st.subheader("📈 Numeric Visualization")
            selected_numeric = st.selectbox(
                "Select numeric column",
                numeric_columns,
                key="eda_numeric"
            )

            fig = VisualizationEngine.histogram(
                data,
                selected_numeric
            )
            st.plotly_chart(fig, width="stretch")

        if categorical_columns:
            st.subheader("📊 Categorical Visualization")
            selected_category = st.selectbox(
                "Select categorical column",
                categorical_columns,
                key="eda_category"
            )

            fig = VisualizationEngine.bar_chart(
                data,
                selected_category
            )
            st.plotly_chart(fig, width="stretch")

    else:
        st.info("Upload a CSV dataset to perform EDA.")


# ============================================================
# MACHINE LEARNING
# ============================================================

elif page == "🤖 Machine Learning":

    st.header("🤖 Machine Learning")
    st.write(
        "Train classification or regression models on uploaded datasets."
    )

    uploaded = st.file_uploader(
        "Upload ML dataset CSV",
        type=["csv"],
        key="ml_csv"
    )

    if uploaded:
        data = pd.read_csv(uploaded)

        st.dataframe(
            data.head(),
            width="stretch"
        )

        target = st.selectbox(
            "Select target column",
            data.columns.tolist(),
            key="ml_target"
        )

        task = st.radio(
            "Machine Learning Task",
            ["Classification", "Regression"],
            horizontal=True
        )

        if task == "Classification":
            model_name = st.selectbox(
                "Select Classification Model",
                [
                    "Random Forest",
                    "Logistic Regression",
                    "Decision Tree"
                ]
            )
        else:
            model_name = st.selectbox(
                "Select Regression Model",
                [
                    "Random Forest",
                    "Linear Regression"
                ]
            )

        if st.button(
            "🤖 Train Machine Learning Model",
            type="primary"
        ):
            try:
                ml = MLAnalyzer(data)

                if task == "Classification":
                    result = ml.classification(
                        target,
                        model_name
                    )

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric(
                        "Accuracy",
                        f"{result['accuracy']:.2%}"
                    )
                    c2.metric(
                        "Precision",
                        f"{result['precision']:.2%}"
                    )
                    c3.metric(
                        "Recall",
                        f"{result['recall']:.2%}"
                    )
                    c4.metric(
                        "F1 Score",
                        f"{result['f1']:.2%}"
                    )

                else:
                    result = ml.regression(
                        target,
                        model_name
                    )

                    c1, c2, c3 = st.columns(3)
                    c1.metric(
                        "R²",
                        f"{result['r2']:.4f}"
                    )
                    c2.metric(
                        "MAE",
                        f"{result['mae']:.4f}"
                    )
                    c3.metric(
                        "RMSE",
                        f"{result['rmse']:.4f}"
                    )

                st.success(
                    f"{model_name} trained successfully."
                )

            except Exception as e:
                st.error(f"Machine learning error: {e}")

    else:
        st.info("Upload a dataset CSV to train a machine-learning model.")


# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

elif page == "🕸️ Knowledge Graph":

    st.header("🕸️ Interactive Knowledge Graph")
    st.write(
        "Explore relationships between conversations, speakers, "
        "languages, events and transcripts."
    )

    try:
        from streamlit_agraph import agraph, Node, Edge, Config

        if df.empty:
            st.info("No conversation data available.")
        else:
            nodes = []
            edges = []
            node_ids = set()
            edge_ids = set()

            def add_node(node_id, label, size=25):
                if node_id not in node_ids:
                    nodes.append(
                        Node(
                            id=node_id,
                            label=label,
                            size=size,
                            shape="dot"
                        )
                    )
                    node_ids.add(node_id)

            def add_edge(source, target, label):
                edge_key = f"{source}__{target}__{label}"
                if edge_key not in edge_ids:
                    edges.append(
                        Edge(
                            source=source,
                            target=target,
                            label=label
                        )
                    )
                    edge_ids.add(edge_key)

            for _, row in df.iterrows():
                conversation_id = str(row["id"])
                conversation_node = f"conversation_{conversation_id}"

                add_node(
                    conversation_node,
                    f"Conversation {conversation_id}",
                    35
                )

                speaker = row["speaker"]
                if pd.notna(speaker):
                    speaker_node = (
                        "speaker_" +
                        str(speaker).replace(" ", "_")
                    )
                    add_node(
                        speaker_node,
                        str(speaker),
                        30
                    )
                    add_edge(
                        speaker_node,
                        conversation_node,
                        "SPOKE_IN"
                    )

                language = row["language"]
                if pd.notna(language):
                    language_node = (
                        "language_" +
                        str(language).replace(" ", "_")
                    )
                    add_node(
                        language_node,
                        str(language),
                        30
                    )
                    add_edge(
                        conversation_node,
                        language_node,
                        "HAS_LANGUAGE"
                    )

                transcript = row["transcript"]
                if pd.notna(transcript):
                    transcript_node = f"transcript_{conversation_id}"
                    short_text = str(transcript)
                    if len(short_text) > 35:
                        short_text = short_text[:35] + "..."
                    add_node(
                        transcript_node,
                        short_text,
                        20
                    )
                    add_edge(
                        conversation_node,
                        transcript_node,
                        "HAS_TRANSCRIPT"
                    )

                for index, event in enumerate(
                    parse_events(row["events"])
                ):
                    if isinstance(event, dict):
                        event_type = event.get("type", "Unknown")
                    else:
                        event_type = str(event)

                    event_node = (
                        f"event_{conversation_id}_{index}"
                    )
                    add_node(
                        event_node,
                        event_type,
                        25
                    )
                    add_edge(
                        conversation_node,
                        event_node,
                        "HAS_EVENT"
                    )

            config = Config(
                width="100%",
                height=650,
                directed=True,
                physics=True,
                hierarchical=False,
                nodeHighlightBehavior=True,
                highlightColor="#F7A072",
                collapsible=False
            )

            agraph(
                nodes=nodes,
                edges=edges,
                config=config
            )

            col1, col2 = st.columns(2)
            col1.metric("🔵 Nodes", len(nodes))
            col2.metric("🔗 Relationships", len(edges))

    except ImportError:
        st.error("streamlit-agraph is not installed.")
        st.code("pip install streamlit-agraph")
    except Exception as e:
        st.error(f"Knowledge Graph error: {e}")


# ============================================================
# CONVERSATION DATABASE
# ============================================================

elif page == "💾 Conversation Database":

    st.header("💾 Conversation Database")

    if df.empty:
        st.info("No conversations stored.")
    else:
        st.write(f"Total conversations: **{len(df)}**")

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

        st.markdown("---")
        st.subheader("📥 Export Database")

        csv_data = df.to_csv(index=False)

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="voxintel_conversations.csv",
            mime="text/csv"
        )


# ============================================================
# CONVERSATION ANALYTICS
# ============================================================

elif page == "📈 Analytics":

    st.header("📈 Conversation Analytics")

    if df.empty:
        st.info("No conversation data available.")
    else:
        st.subheader("🌐 Language Analytics")

        language_distribution = (
            df["language"]
            .fillna("Unknown")
            .value_counts()
        )

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(language_distribution)

        with col2:
            st.dataframe(
                language_distribution
                .rename("Conversations")
                .to_frame(),
                width="stretch"
            )

        st.markdown("---")
        st.subheader("👤 Speaker Analytics")

        speaker_distribution = (
            df["speaker"]
            .fillna("Unknown")
            .value_counts()
        )

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(speaker_distribution)

        with col2:
            st.dataframe(
                speaker_distribution
                .rename("Conversations")
                .to_frame(),
                width="stretch"
            )

        st.markdown("---")
        st.subheader("📝 Conversation Length")

        word_counts = [
            len(str(text).split())
            for text in df["transcript"]
        ]

        word_df = pd.DataFrame({
            "Conversation": df["id"],
            "Words": word_counts
        })

        st.bar_chart(
            word_df.set_index("Conversation")
        )

        st.markdown("---")
        st.subheader("🧠 Event Analytics")

        counts = event_counts(df)

        if counts:
            event_df = pd.DataFrame(
                list(counts.items()),
                columns=["Event", "Count"]
            )

            st.bar_chart(
                event_df.set_index("Event")
            )

            st.dataframe(
                event_df,
                width="stretch",
                hide_index=True
            )
        else:
            st.info("No events available.")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "VOXINTEL — AI-Powered Multilingual Conversation & "
    "Customer Intelligence Platform"
)

st.caption(
    "Speech → Text → Language → Speaker → Events → "
    "Memory → Database → NLP → Customer Intelligence → "
    "Data Science → Business Insights"
)
