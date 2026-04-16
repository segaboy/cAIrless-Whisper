# cAIrless-Whisper

A command-line tool that transcribes audio files to timestamped text using [OpenAI Whisper](https://github.com/openai/whisper). Supports MP3, MP4, WAV, M4A, FLAC, and other common formats.

Transcripts are saved as plain text files with per-segment timestamps, plus a clean full-text section at the end, ready for searching, summarizing, or archiving.

---

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org) installed and on your PATH
- openai-whisper Python package

---

## Installation

**1. Install Python** (if not already installed)
```bash
winget install Python.Python.3.12   # Windows
brew install python                 # macOS
```

**2. Install ffmpeg**
```bash
winget install Gyan.FFmpeg   # Windows
brew install ffmpeg          # macOS
sudo apt install ffmpeg      # Debian-based Linux
sudo dnf install ffmpeg      # RPM-based Linux
```

**3. Install Whisper**
```bash
pip install openai-whisper
```

> The first time you run the script, Whisper will download the selected model. Subsequent runs use the cached version.

---

## Usage

```bash
# Basic — uses the 'base' model by default
python cairlesswhisper.py audio.mp3

# Specify a larger model for better accuracy
python cairlesswhisper.py audio.mp3 --model medium

# Specify output file location
python cairlesswhisper.py audio.mp3 --output transcript.txt

# Hint the language for faster, more accurate results
python cairlesswhisper.py audio.mp3 --language en

# Run without arguments — prompts for file path interactively
python cairlesswhisper.py
```

---

## Model Sizes

| Model  | Size   | Speed    | Accuracy |
|--------|--------|----------|----------|
| tiny   | ~75MB  | Fastest  | Basic    |
| base   | ~140MB | Fast     | Good     |
| small  | ~460MB | Moderate | Better   |
| medium | ~1.5GB | Slow     | High     |
| large  | ~3GB   | Slowest  | Best     |

The `base` model handles most use cases well. Use `medium` or `large` for content with heavy accents, technical jargon, or noisy audio.

---

## Output Format

Transcripts are saved as `.txt` files alongside the source audio (or at a path you specify with `--output`). Each file contains:

- A timestamped section with one line per segment
- A full-text section with no timestamps (useful for searching or copying)

**Example output:**
```
TRANSCRIPT: interview.mp3
============================================================

[00:00] Welcome to the show.
[00:07] Today we're talking about engineering leadership.
[00:14] My guest has spent over 17 years building distributed systems...

============================================================
Full text (no timestamps):
============================================================
Welcome to the show. Today we're talking about engineering leadership...
```

---

## Dependencies

- [openai-whisper](https://github.com/openai/whisper) — OpenAI's speech recognition model
- [ffmpeg](https://ffmpeg.org) — audio decoding backend used by Whisper

---

## License

MIT
