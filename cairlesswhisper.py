"""
whisper-transcriber
-------------------
Transcribes audio files to timestamped text using OpenAI Whisper.
Supports MP3, MP4, WAV, M4A, FLAC, and other common audio formats.

Requirements:
    pip install openai-whisper
    ffmpeg (https://ffmpeg.org) must be installed and on PATH

Usage:
    python cairlesswhisper.py audio.mp3
    python cairlesswhisper.py audio.mp3 --model medium
    python cairlesswhisper.py audio.mp3 --output my_transcript.txt
    python cairlesswhisper.py audio.mp3 --language en
"""

import sys
import os
import argparse


MODELS = {
    "tiny":   "Fastest, least accurate (~75MB)",
    "base":   "Good balance of speed and accuracy (~140MB)  [default]",
    "small":  "Better accuracy, slower (~460MB)",
    "medium": "High accuracy, significantly slower (~1.5GB)",
    "large":  "Best accuracy, slowest (~3GB)",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files to timestamped text using OpenAI Whisper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n".join(f"  {k:8s} — {v}" for k, v in MODELS.items()),
    )
    parser.add_argument(
        "audio",
        nargs="?",
        help="Path to the audio file to transcribe",
    )
    parser.add_argument(
        "--model", "-m",
        default="base",
        choices=MODELS.keys(),
        help="Whisper model size (default: base)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: same location as audio, with _transcript.txt suffix)",
    )
    parser.add_argument(
        "--language", "-l",
        default=None,
        help="Language code to improve accuracy, e.g. 'en', 'es' (default: auto-detect)",
    )
    return parser.parse_args()


def check_ffmpeg():
    import shutil
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed or not on your PATH.")
        print("Install it with:  winget install Gyan.FFmpeg  (Windows)")
        print("                  brew install ffmpeg          (macOS)")
        print("                  sudo apt install ffmpeg      (Linux)")
        sys.exit(1)


def load_whisper(model_size):
    try:
        import whisper
    except ImportError:
        print("openai-whisper not found. Installing now...")
        os.system(f"{sys.executable} -m pip install openai-whisper")
        import whisper
    print(f"Loading Whisper '{model_size}' model — {MODELS[model_size]}")
    print("(First run will download the model. Subsequent runs use the cached version.)\n")
    return whisper.load_model(model_size)


def format_timestamp(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"[{m:02d}:{s:02d}]"


def build_transcript(filename, result):
    lines = [
        f"TRANSCRIPT: {filename}",
        "=" * 60,
        "",
    ]
    for segment in result["segments"]:
        ts = format_timestamp(segment["start"])
        lines.append(f"{ts} {segment['text'].strip()}")

    lines += [
        "",
        "=" * 60,
        "Full text (no timestamps):",
        "=" * 60,
        result["text"].strip(),
    ]
    return "\n".join(lines)


def main():
    args = parse_args()

    # Prompt for file if not provided
    audio_path = args.audio
    if not audio_path:
        audio_path = input("Enter the path to your audio file: ").strip().strip('"')

    audio_path = os.path.abspath(audio_path)

    if not os.path.exists(audio_path):
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)

    check_ffmpeg()

    # Determine output path
    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        base = os.path.splitext(audio_path)[0]
        output_path = base + "_transcript.txt"

    model = load_whisper(args.model)

    print(f"Transcribing: {os.path.basename(audio_path)}")
    if args.language:
        print(f"Language: {args.language}")
    print("This may take a few minutes for longer files...\n")

    result = model.transcribe(
        audio_path,
        verbose=False,
        language=args.language,
    )

    transcript = build_transcript(os.path.basename(audio_path), result)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    duration = result["segments"][-1]["end"] if result["segments"] else 0
    m, s = int(duration // 60), int(duration % 60)

    print(f"Done.")
    print(f"  Audio duration : {m:02d}:{s:02d}")
    print(f"  Segments       : {len(result['segments'])}")
    print(f"  Output         : {output_path}")
    print(f"\nPreview:\n{result['text'][:300].strip()}...")


if __name__ == "__main__":
    main()
