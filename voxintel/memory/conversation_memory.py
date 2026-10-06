import json
import os
from datetime import datetime


class ConversationMemory:

    def __init__(self, file_path="conversation_memory.json"):

        self.file_path = file_path
        self.conversations = []

        self.load_memory()

    def load_memory(self):

        if os.path.exists(self.file_path):

            try:
                with open(
                    self.file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.conversations = json.load(file)

            except (json.JSONDecodeError, OSError):

                self.conversations = []

    def add_conversation(
        self,
        speaker,
        text,
        language,
        events=None
    ):

        conversation = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "text": text,
            "language": language,
            "events": events or []
        }

        self.conversations.append(conversation)

        self.save_memory()

    def save_memory(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.conversations,
                file,
                indent=4,
                ensure_ascii=False
            )

    def get_all_conversations(self):

        return self.conversations

    def clear_memory(self):

        self.conversations = []

        self.save_memory()


if __name__ == "__main__":

    memory = ConversationMemory()

    print("VOXINTEL Conversation Memory Test")
    print("=" * 50)

    memory.add_conversation(
        speaker="Speaker 1",
        text="Hello, this is my VOXINTEL test.",
        language="English",
        events=[]
    )

    memory.add_conversation(
        speaker="Speaker 2",
        text="We have a meeting at 10 AM.",
        language="English",
        events=[
            {
                "type": "Meeting"
            },
            {
                "type": "Time",
                "value": "10 AM"
            }
        ]
    )

    print("\nStored Conversations:")

    for conversation in memory.get_all_conversations():

        print("-" * 50)

        print("Speaker:",
              conversation["speaker"])

        print("Text:",
              conversation["text"])

        print("Language:",
              conversation["language"])

        print("Events:",
              conversation["events"])