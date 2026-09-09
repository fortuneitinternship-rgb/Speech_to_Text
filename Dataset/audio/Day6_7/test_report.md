# Speech-to-Text Test Report

## Objective
To test speech-to-text conversion under different speaking conditions.

## Test Results

| Test Case | Condition | Result |
|---|---|---|
| 1 | Normal voice | Successful |
| 2 | Loud voice | Successful |
| 3 | Low voice | Successful |
| 4 | Fast speech | Successful |
| 5 | Slow speech | Successful |
| 6 | Short pauses | Successful |
| 7 | Background noise | Successful |
| 8 | No speech | Error handled successfully |

## Observations
The speech recognition system successfully converted spoken words into text under different conditions. Background noise was handled using ambient-noise adjustment.

## Errors Handled
- No speech detected
- Unclear speech
- Speech recognition service unavailable
- Microphone or other unexpected errors

## Conclusion
The Speech-to-Text module was successfully implemented and tested using Python SpeechRecognition. The system can capture live voice and convert it into text with appropriate error handling.