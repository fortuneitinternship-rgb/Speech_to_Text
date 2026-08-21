import pyaudio
import wave
import os

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
OUTPUT_FILE = "audio/recording.wav"

audio = pyaudio.PyAudio()

print("Voice Translator - Audio Test")

# Check microphone
try:
    audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    ).close()

    print("\nMicrophone detected successfully.")
except Exception as e:
    print("Microphone not detected.")
    print(e)
    audio.terminate()
    exit()

print("\nRecording started...")
print("Speak now...")

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
audio.terminate()

print("\nRecording stopped.")

os.makedirs("audio", exist_ok=True)

with wave.open(OUTPUT_FILE, "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))

print("\nAudio saved successfully:")
print(OUTPUT_FILE)
print("\nRecording Completed")