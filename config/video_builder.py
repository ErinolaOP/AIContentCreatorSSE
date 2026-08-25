import os
import subprocess
import imageio_ffmpeg

def get_audio_duration(ffmpeg_exe: str, audio_path: str) -> float:
    """Uses ffprobe to extract the exact length of the voiceover audio in seconds."""
    ffprobe_exe = ffmpeg_exe.replace("ffmpeg", "ffprobe")
    cmd = [
        ffprobe_exe, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except Exception:
        return 35.0  # Fallback estimate

def assemble_video(video_paths: list, audio_path: str, output_path: str = "generated/base_video.mp4") -> str:
    """Loops and trims video clips dynamically to ensure full coverage of the audio track."""
    valid_paths = [p for p in video_paths if os.path.exists(p)]
    if not valid_paths:
        raise FileNotFoundError("No valid video clips found on disk.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # Step 1: Calculate segment duration per clip
    audio_duration = get_audio_duration(ffmpeg_exe, audio_path)
    num_clips = len(valid_paths)
    
    # Calculate exact duration each clip must cover (+1s overlap buffer)
    clip_duration = (audio_duration / num_clips) + 1.0
    print(f"🎙️ Audio Duration: {audio_duration:.2f}s | Forcing {num_clips} clips to {clip_duration:.2f}s each...")

    # Step 2: Loop & normalize each clip so short videos don't cut the timeline short
    normalized_clips = []
    for idx, path in enumerate(valid_paths):
        norm_path = f"generated/raw_clips/norm_{idx}.mp4"
        filter_str = "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30"
        
        cmd = [
            ffmpeg_exe, "-y",
            "-stream_loop", "-1",  # Loop clip continuously so it never runs out of frames
            "-ss", "00:00:00",
            "-i", path,
            "-t", str(clip_duration), # Hard trim at exact needed segment length
            "-vf", filter_str,
            "-c:v", "libx264",
            "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-an",
            norm_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(norm_path):
            normalized_clips.append(norm_path)

    # Step 3: Write concat list
    concat_list_path = "generated/concat_list.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for path in normalized_clips:
            abs_path = os.path.abspath(path).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")

    # Step 4: Stitch and clamp precisely to voiceover end
    command = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    print("Stitching looped clips to full audio length...")
    subprocess.run(command, check=True)

    if os.path.exists(concat_list_path):
        os.remove(concat_list_path)

    return output_path