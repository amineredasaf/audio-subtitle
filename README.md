# 🎧 Audio Transcription API with Vosk + FastAPI

"In the process of uploading my abandoned project from my PC that I never pushed."
This project provides a simple API that accepts audio files (MP3, WAV, etc.) and returns subtitle content in SRT format using the [Vosk](https://alphacephei.com/vosk/) speech recognition engine.

---

## 🚀 Features

- Accepts audio files via HTTP POST
- Converts audio to 16kHz mono WAV using FFmpeg
- Transcribes speech to text using Vosk
- Returns subtitles in `.srt` format
- Lightweight and fast, thanks to FastAPI

---

## 🛠️ Requirements

- Python 3.7+
- `ffmpeg` installed on your system
- A Vosk speech recognition model (e.g., English: `vosk-model-small-en-us-0.15`)

---

## 🧪 Quick Setup

1. **Clone the repo** https://github.com/amineredasaf/audio-subtitle.git:

2. **Make setup script executable** and run it:
   ```bash
   chmod +x requirement.sh
   ./requirement.sh
