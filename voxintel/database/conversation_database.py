import sqlite3
from datetime import datetime


class ConversationDatabase:

    def __init__(self, db_path="voxintel.db"):
        self.db_path = db_path
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                transcript TEXT NOT NULL,
                language TEXT,
                speaker TEXT,
                events TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_conversation(
        self,
        transcript,
        language,
        speaker,
        events
    ):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations
            (timestamp, transcript, language, speaker, events)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            transcript,
            language,
            speaker,
            str(events)
        ))

        conn.commit()
        conn.close()

    def get_all_conversations(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, timestamp, transcript,
                   language, speaker, events
            FROM conversations
            ORDER BY id DESC
        """)

        conversations = cursor.fetchall()

        conn.close()

        return conversations

    def get_conversation_count(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM conversations"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count