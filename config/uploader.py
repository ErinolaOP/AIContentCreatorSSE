import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """Authenticates the user using client_secrets.json and saves token.pickle."""
    credentials = None
    token_file = "token.pickle"
    client_secrets_file = "client_secrets.json"

    if not os.path.exists(client_secrets_file):
        raise FileNotFoundError(
            f"Missing '{client_secrets_file}'. Ensure it is placed directly in your root project directory."
        )

    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(token_file, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def upload_to_youtube(video_path: str, title: str, description: str, tags: list = None) -> str:
    """Uploads a video file to YouTube Shorts."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at: {video_path}")

    youtube = get_authenticated_service()

    if tags is None:
        tags = ["Shorts", "Viral", "Motivation"]

    full_title = f"{title} #Shorts" if "#Shorts" not in title else title

    body = {
        "snippet": {
            "title": full_title[:100],
            "description": f"{description}\n\n#Shorts #{' #'.join(tags)}",
            "tags": tags,
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")

    print(f"\n📤 Uploading '{full_title}' to YouTube...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%...")

    video_id = response.get("id")
    video_url = f"https://youtube.com/shorts/{video_id}"
    print(f"🎉 Successfully Uploaded! Short URL: {video_url}")
    return video_url