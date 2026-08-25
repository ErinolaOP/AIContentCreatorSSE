import os
import requests

def fetch_broll_clips(keywords: list, output_dir: str = "generated/raw_clips") -> list:
    """Fetches vertical B-roll video clips from Pexels based on search keywords."""
    pexels_api_key = os.getenv("PEXELS_API_KEY")
    if not pexels_api_key:
        raise ValueError("PEXELS_API_KEY environment variable is missing from your .env file.")

    os.makedirs(output_dir, exist_ok=True)
    downloaded_paths = []
    headers = {"Authorization": pexels_api_key}

    for idx, query in enumerate(keywords):
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("videos"):
                video_files = data["videos"][0]["video_files"]
                # Get the direct download URL for the clip
                download_url = video_files[0]["link"]
                
                file_path = os.path.join(output_dir, f"clip_{idx}.mp4")
                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                downloaded_paths.append(file_path)
                print(f"Downloaded clip for '{query}': {file_path}")

    return downloaded_paths