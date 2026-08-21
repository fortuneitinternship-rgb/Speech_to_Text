
# Audio Concepts Notes
Audio Concepts Notes

1. What is Audio?

Audio is a sound signal produced by vibrations. Human speech creates sound waves that can be captured by a microphone.

2. Analog vs Digital Audio

Analog Audio

Analog audio is a continuous sound signal that changes smoothly over time. A microphone initially receives our voice as an analog signal.

Digital Audio

Digital audio represents sound as numerical data that a computer can process. The analog signal is converted into digital samples using an analog-to-digital converter.

3. Amplitude and Frequency

Amplitude represents the strength or loudness of a sound.

Frequency represents how many cycles of a sound wave occur per second. It is measured in Hertz (Hz). Frequency is related to the pitch of sound.

4. How a Microphone Captures Voice

When we speak, our voice produces sound waves. The microphone detects these sound waves and converts them into an electrical signal. The computer then converts the signal into digital audio data.

Python can access the microphone through audio libraries such as PyAudio or sounddevice.

5. Audio Sampling

Sampling is the process of measuring an analog audio signal at regular intervals and converting those measurements into digital values.

Common Sample Rates

- 8,000 Hz – commonly used in telephone-quality audio.
- 16,000 Hz – commonly used for speech-processing applications.
- 44,100 Hz – commonly used for music and general audio.
- 48,000 Hz – commonly used in video and professional audio.

A sample rate of 16 kHz means that the audio signal is measured 16,000 times per second.

6. Mono vs Stereo

Mono Audio

Mono uses one audio channel. The same audio signal is recorded through a single channel.

Stereo Audio

Stereo uses two audio channels, usually left and right.

Speech applications often use mono audio because speech usually does not require separate left and right channels. Mono also reduces the amount of audio data that needs to be processed.

7. WAV Audio Format

WAV is an audio file format commonly used for storing uncompressed digital audio. It is useful for speech-processing projects because it preserves the recorded audio data without the compression commonly used in formats such as MP3.

In this project, the recorded voice is saved as:

"audio/recording.wav"

8. Basic Audio Processing Concepts

Background Noise

Unwanted sounds such as fans, traffic, keyboard sounds, or people talking in the background.

Silence

A period where there is little or no speech signal.

Volume / Amplitude

The amplitude of an audio signal is related to the strength or loudness of the sound.

Noise Reduction

The process of reducing unwanted background sounds from an audio recording.

Voice Activity

Voice activity detection identifies portions of an audio signal where a person is speaking.

Audio Normalization

Normalization adjusts the audio level so that the recording has a more consistent volume.

9. Python Audio Libraries

SpeechRecognition

A Python library that provides an interface for speech recognition systems and can be used to convert speech into text.

PyAudio

A Python library used to access audio input and output devices such as microphones and speakers.

wave

Python's built-in "wave" module can read and write WAV audio files.

sounddevice

A Python library that can be used to record and play audio through audio devices.

10. Practical Recording

The practical program performs the following steps:

1. Start the program.
2. Detect the microphone.
3. Start recording.
4. Record the user's voice.
5. Stop recording.
6. Save the audio as a WAV file.
7. Display "Recording Completed".

The recorded audio was successfully saved as:

"audio/recording.wav"

11. Recording Quality

The recorded audio was played back after recording to verify that the voice was captured successfully.

The recording can be affected by background noise, microphone quality, speaking distance, and recording volume.

Conclusion

This task helped me understand how a computer receives voice through a microphone, converts the analog sound into digital audio samples, records the audio using Python, and saves it as a WAV file for further speech-processing applications.
