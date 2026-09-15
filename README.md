## Task 05: Connect Microphone with Python and Capture Voice Input

### Objective

To connect the system microphone with Python and capture voice input successfully.

### Implementation

The `SpeechRecognition` and `PyAudio` libraries were used to detect and access the microphone. The program adjusts for background noise and listens for the user's voice input.

### Workflow

1. Detect the available microphone.
2. Connect Python to the microphone.
3. Adjust for ambient/background noise.
4. Listen for voice input.
5. Capture the user's voice.
6. Confirm that audio input was received successfully.

### Result

The microphone was successfully detected and connected with Python. Voice input was captured successfully, completing Task 05.

### File Created

`audio/microphone_test.py`

## Task 06: Convert Voice Input into Text

### Objective

To convert captured voice input from the microphone into text using Python.

### Implementation

The `SpeechRecognition` library and Google Speech Recognition service were used to process the captured audio and convert speech into readable text.

### Workflow

1. Connect to the microphone.
2. Adjust for background noise.
3. Capture the user's voice.
4. Process the captured audio.
5. Convert speech into text.
6. Display the recognized text.

### Result

The voice input was successfully captured and converted into text using Python.

### File Created

`audio/speech_to_text.py`


## Day 6 & 7 – Speech-to-Text Conversion

### Objective
Implemented and tested live speech-to-text conversion using Python SpeechRecognition.

### Features
- Captures voice through the microphone
- Adjusts for background noise
- Converts speech into text
- Displays recognized text
- Handles no speech and unclear speech
- Uses timeout and phrase time limits
- Tested with different voices, speeds, pauses, and background noise

### Listening Parameters
- Energy Threshold: 300
- Pause Threshold: 0.8 seconds
- Phrase Threshold: 0.3 seconds
- Timeout: 5 seconds
- Phrase Time Limit: 10 seconds

### Testing
The system was tested under normal voice, loud voice, low voice, fast speech, slow speech, pauses, background noise, and no-speech conditions.

### Result
Speech-to-text conversion was successfully implemented and tested with appropriate error handling.


## Task 7 – Language Detection and Basic Text Translation

### Objective

Implement language detection and basic text translation for recognized speech text using Python and a translation library/API.

### Languages Tested

* English (`en`)
* Hindi (`hi`)
* Marathi (`mr`)
* Telugu (`te`)
* Tamil (`ta`)

### Test Results

#### 1. English → Marathi

![English to Marathi](Dataset/audio/screenshots/English%20to%20marathi%20text.png)

#### 2. Marathi → English

![Marathi to English](Dataset/audio/screenshots/Marathi%20to%20english%20text.png)

#### 3. English → Tamil

![English to Tamil](Dataset/audio/screenshots/english%20to%20tamil%20text.png)

#### 4. Hindi → English

![Hindi to English](Dataset/audio/screenshots/hindi%20to%20english%20text.png)

#### 5. Telugu → English & Tamil → English

![Telugu to English and Tamil to English](Dataset/audio/screenshots/telugu%20to%20english%20%26%20Tamil%20to%20english%20text.png)

### Implementation Files

* `Dataset/Python/language_detection.py`
* `Dataset/Python/translator.py`

### Outcome

Successfully implemented and tested language detection and basic text translation for multiple languages.

