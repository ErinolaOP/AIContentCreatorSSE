import os
import imageio_ffmpeg
import whisper
from whisper.audio import load_audio

# Grab the exact location of the embedded ffmpeg.exe binary
FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

def custom_load_audio(file: str, sr: int = 16000):
    """Overrides Whisper's default audio loader to use our exact FFmpeg path."""
    import subprocess
    import numpy as np

    cmd = [
        FFMPEG_PATH,
        "-nostdin",
        "-threads", "0",
        "-i", file,
        "-f", "s16le",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        "-ar", str(sr),
        "-"
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

# Direct override of Whisper's internal audio loader
whisper.audio.load_audio = custom_load_audio

def generate_subtitles(audio_path: str = "generated/audio/voiceover.mp3"):
    """Transcribes audio file and returns word-level timestamps."""
    # Convert relative path to absolute path to avoid directory confusion
    abs_audio_path = os.path.abspath(audio_path)
    
    if not os.path.exists(abs_audio_path):
        raise FileNotFoundError(f"Audio file not found at: {abs_audio_path}")

    print("Loading Whisper AI model...")
    model = whisper.load_model("base")

    print(f"Transcribing audio: {abs_audio_path}...")
    result = model.transcribe(abs_audio_path, word_timestamps=True)

    words_data = []
    print("\n--- Timestamped Words ---")
    for segment in result.get("segments", []):
        for word in segment.get("words", []):
            word_info = {
                "word": word["word"].strip(),
                "start": round(word["start"], 2),
                "end": round(word["end"], 2)
            }
            words_data.append(word_info)
            print(f"[{word_info['start']}s -> {word_info['end']}s] {word_info['word']}")

    return words_data

if __name__ == "__main__":
    generate_subtitles()