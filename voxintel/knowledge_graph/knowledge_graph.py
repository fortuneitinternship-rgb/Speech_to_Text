import sqlite3
import ast


class KnowledgeGraph:

    def __init__(self, db_path="voxintel.db"):

        self.db_path = db_path

        self.nodes = []
        self.relationships = []

    # ----------------------------------------
    # LOAD DATA FROM SQLITE
    # ----------------------------------------

    def load_conversations(self):

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, transcript, language, speaker, events
            FROM conversations
            ORDER BY id
        """)

        conversations = cursor.fetchall()

        conn.close()

        return conversations

    # ----------------------------------------
    # ADD NODE
    # ----------------------------------------

    def add_node(self, node_id, node_type, label):

        node = {
            "id": node_id,
            "type": node_type,
            "label": label
        }

        if node not in self.nodes:
            self.nodes.append(node)

    # ----------------------------------------
    # ADD RELATIONSHIP
    # ----------------------------------------

    def add_relationship(
        self,
        source,
        relationship,
        target
    ):

        edge = {
            "source": source,
            "relationship": relationship,
            "target": target
        }

        if edge not in self.relationships:
            self.relationships.append(edge)

    # ----------------------------------------
    # BUILD KNOWLEDGE GRAPH
    # ----------------------------------------

    def build_graph(self):

        conversations = self.load_conversations()

        for row in conversations:

            conversation_id = row[0]
            transcript = row[1]
            language = row[2]
            speaker = row[3]
            events_data = row[4]

            conversation_node = (
                f"conversation_{conversation_id}"
            )

            # Conversation
            self.add_node(
                conversation_node,
                "Conversation",
                f"Conversation {conversation_id}"
            )

            # Speaker
            if speaker:

                speaker_node = (
                    f"speaker_{speaker.replace(' ', '_')}"
                )

                self.add_node(
                    speaker_node,
                    "Speaker",
                    speaker
                )

                self.add_relationship(
                    speaker_node,
                    "SPOKE_IN",
                    conversation_node
                )

            # Language
            if language:

                language_node = (
                    f"language_{language.replace(' ', '_')}"
                )

                self.add_node(
                    language_node,
                    "Language",
                    language
                )

                self.add_relationship(
                    conversation_node,
                    "HAS_LANGUAGE",
                    language_node
                )

            # Transcript
            if transcript:

                transcript_node = (
                    f"transcript_{conversation_id}"
                )

                self.add_node(
                    transcript_node,
                    "Transcript",
                    transcript
                )

                self.add_relationship(
                    conversation_node,
                    "HAS_TRANSCRIPT",
                    transcript_node
                )

            # Events
            if events_data:

                try:

                    events = ast.literal_eval(
                        events_data
                    )

                except (ValueError, SyntaxError):

                    events = []

                if events:

                    for index, event in enumerate(events):

                        if isinstance(event, dict):

                            event_type = event.get(
                                "type",
                                "Unknown"
                            )

                        else:

                            event_type = str(event)

                        event_node = (
                            f"event_{conversation_id}_{index}"
                        )

                        self.add_node(
                            event_node,
                            "Event",
                            event_type
                        )

                        self.add_relationship(
                            conversation_node,
                            "HAS_EVENT",
                            event_node
                        )

        return self

    # ----------------------------------------
    # DISPLAY GRAPH
    # ----------------------------------------

    def display_graph(self):

        print("\n" + "=" * 60)
        print(
            "             VOXINTEL KNOWLEDGE GRAPH"
        )
        print("=" * 60)

        print("\nNodes:")

        if not self.nodes:

            print("  No nodes found.")

        else:

            for node in self.nodes:

                print(
                    f"  [{node['type']}] "
                    f"{node['label']}"
                )

        print("\nRelationships:")

        if not self.relationships:

            print("  No relationships found.")

        else:

            for relationship in self.relationships:

                source = relationship["source"]
                relation = relationship["relationship"]
                target = relationship["target"]

                source_label = next(
                    (
                        node["label"]
                        for node in self.nodes
                        if node["id"] == source
                    ),
                    source
                )

                target_label = next(
                    (
                        node["label"]
                        for node in self.nodes
                        if node["id"] == target
                    ),
                    target
                )

                print(
                    f"  {source_label} "
                    f"--[{relation}]--> "
                    f"{target_label}"
                )

        print("\nGraph Statistics:")

        print(
            "  Total Nodes:",
            len(self.nodes)
        )

        print(
            "  Total Relationships:",
            len(self.relationships)
        )

        print("\n" + "=" * 60)


# ----------------------------------------
# TEST
# ----------------------------------------

if __name__ == "__main__":

    graph = KnowledgeGraph()

    graph.build_graph()

    graph.display_graph()