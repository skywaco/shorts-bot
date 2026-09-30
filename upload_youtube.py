import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import YOUTUBE_CLIENT_FILE

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "logs/youtube_token.pickle"

def get_youtube_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(YOUTUBE_CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs("logs", exist_ok=True)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return build("youtube", "v3", credentials=creds)

def upload_to_youtube(video_path: str, title: str, description: str, hashtags: str) -> str:
    """Upload video to YouTube Shorts. Returns video URL."""
    yt = get_youtube_service()

    full_desc = f"{description}\n\n{hashtags}\n\n#shorts"

    body = {
        "snippet": {
            "title": title[:100],
            "description": full_desc[:5000],
            "tags": [t.lstrip("#") for t in hashtags.split()],
            "categoryId": "22",   # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    print("  Uploading to YouTube …")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            print(f"  Upload progress: {int(status.progress() * 100)}%")

    video_id = response["id"]
    url = f"https://youtube.com/shorts/{video_id}"
    print(f"  YouTube URL: {url}")
    return url
