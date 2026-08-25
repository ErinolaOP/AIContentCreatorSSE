import os
import subprocess
import imageio_ffmpeg

def create_srt_file(words: list, output_srt: str = "generated/subtitles.srt", words_per_caption: int = 3) -> str:
    """Formats Whisper word timestamps into a clean .srt subtitle file."""
    os.makedirs(os.path.dirname(output_srt), exist_ok=True)
    
    def format_time(seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        msecs = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

    chunks = [words[i:i + words_per_caption] for i in range(0, len(words), words_per_caption)]
    
    with open(output_srt, "w", encoding="utf-8") as f:
        for idx, chunk in enumerate(chunks, 1):
            if not chunk:
                continue
            start_time = format_time(chunk[0]["start"])
            end_time = format_time(chunk[-1]["end"])
            text = " ".join([w["word"].strip() for w in chunk]).upper()
            
            f.write(f"{idx}\n{start_time} --> {end_time}\n{text}\n\n")

    return output_srt

def burn_captions(video_path: str, srt_path: str, output_path: str = "generated/final_video.mp4") -> str:
    """Burns white Anton captions and clamps video duration strictly to audio length."""
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    srt_clean = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")

    style_opts = (
        "Fontname=Anton,"
        "Fontsize= 13,"
        "PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "BorderStyle=1,"
        "Outline=2,"
        "Shadow=0.5,"
        "Alignment=2,"
        "MarginV=40"
    )

    filter_str = f"subtitles='{srt_clean}':force_style='{style_opts}'"

    # Added -shortest to cut off any remaining trailing video padding
    command = [
        ffmpeg_exe, "-y",
        "-i", video_path,
        "-vf", filter_str,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    print("Burning captions and hard-clamping final video duration...")
    subprocess.run(command, check=True)
    return output_path