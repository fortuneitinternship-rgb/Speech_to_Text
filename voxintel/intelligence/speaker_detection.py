class SpeakerDetector:

    def __init__(self):
        self.speaker_count = 0
        self.speakers = {}

    def assign_speaker(self, speaker_id):

        if speaker_id not in self.speakers:
            self.speaker_count += 1

            self.speakers[speaker_id] = (
                f"Speaker {self.speaker_count}"
            )

        return self.speakers[speaker_id]

    def get_speakers(self):

        return self.speakers


if __name__ == "__main__":

    detector = SpeakerDetector()

    print("VOXINTEL Speaker Detection Test")
    print("=" * 40)

    print(detector.assign_speaker("voice_001"))
    print(detector.assign_speaker("voice_002"))
    print(detector.assign_speaker("voice_001"))
    print(detector.assign_speaker("voice_003"))

    print("\nDetected Speakers:")
    print(detector.get_speakers())