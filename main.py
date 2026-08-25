import os
import sys
import json
import random
import shutil
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.script_generator import generate_script
from config.voice_generator import generate_audio
from config.media_fetcher import fetch_broll_clips
from config.video_builder import assemble_video
from config.caption_generator import generate_subtitles
from config.caption_overlay import create_srt_file, burn_captions
from config.uploader import upload_to_youtube

TOPICS_FILE = "topics.json"

def get_and_remove_topic() -> str:
    """Reads topics.json, picks a random topic, and removes it from the queue."""
    if not os.path.exists(TOPICS_FILE):
        raise FileNotFoundError(f"Queue file '{TOPICS_FILE}' was not found.")

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = json.load(f)

    if not topics:
        raise ValueError("All topics in 'topics.json' have been used!")

    selected_topic = random.choice(topics)
    
    if isinstance(selected_topic, dict):
        topic_text = selected_topic.get("topic", "")
    else:
        topic_text = str(selected_topic)

    topics.remove(selected_topic)
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2)

    return topic_text

def cleanup_temp_files():
    """Wipes temporary files if the pipeline fails."""
    print("\n🧹 Cleaning up incomplete build files...")
    temp_folders = ["generated/raw_clips", "generated/audio"]
    temp_files = ["generated/concat_list.txt", "generated/base_video.mp4"]

    for folder in temp_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)

    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)

def run_pipeline():
    """Executes dynamic production and uploads to YouTube."""
    topic = get_and_remove_topic()

    print(f"\n==========================================")
    print(f"🚀 GENERATING & PUBLISHING SHORT FOR: '{topic}'")
    print(f"==========================================\n")

    try:
        print("Step 1/6: Generating script & YouTube metadata...")
        script_data = generate_script(topic)
        
        print("\nStep 2/6: Creating voiceover...")
        voice_path = generate_audio(script_data)

        print("\nStep 3/6: Fetching B-roll footage...")
        video_paths = fetch_broll_clips(script_data["visual_keywords"])

        print("\nStep 4/6: Stitching video & audio...")
        base_video = assemble_video(video_paths, voice_path)

        print("\nStep 5/6: Generating and burning captions...")
        words = generate_subtitles(voice_path)
        srt_path = create_srt_file(words, words_per_caption=3)
        final_video = burn_captions(video_path=base_video, srt_path=srt_path)

        print("\nStep 6/6: Uploading video to YouTube Shorts...")
        video_url = upload_to_youtube(
            video_path=final_video,
            title=script_data.get("title", topic),
            description=script_data.get("description", topic),
            tags=script_data.get("hashtags", ["Shorts"])
        )

        print(f"\n==========================================")
        print(f"🎉 PIPELINE COMPLETE!")
        print(f"🔗 Published Short: {video_url}")
        print(f"==========================================\n")

    except Exception as e:
        print(f"\n❌ PIPELINE ERROR OCCURRED: {e}")
        cleanup_temp_files()
        raise e

if __name__ == "__main__":
    run_pipeline()