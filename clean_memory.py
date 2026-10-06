import json
import os


MEMORY_FILE = "conversation_memory.json"


def clean_memory():

    if not os.path.exists(MEMORY_FILE):

        print("Memory file not found.")
        return

    with open(
        MEMORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        conversations = json.load(file)

    original_count = len(conversations)

    invalid_phrases = [
        "Could not understand the audio.",
        "Speech recognition service error:",
        "Unexpected speech recognition error:"
    ]

    cleaned_conversations = []

    for conversation in conversations:

        text = conversation.get("text", "")

        is_invalid = any(
            phrase in text
            for phrase in invalid_phrases
        )

        if not is_invalid:
            cleaned_conversations.append(conversation)

    removed_count = (
        original_count -
        len(cleaned_conversations)
    )

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cleaned_conversations,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("=" * 50)
    print("VOXINTEL MEMORY CLEANUP")
    print("=" * 50)

    print("Original records:", original_count)
    print("Removed records:", removed_count)
    print("Remaining records:", len(cleaned_conversations))

    print("\nMemory cleanup completed successfully.")


if __name__ == "__main__":

    clean_memory()