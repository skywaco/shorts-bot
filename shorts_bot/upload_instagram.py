import requests
import time
from config import INSTAGRAM_TOKEN, INSTAGRAM_USER_ID

BASE = "https://graph.facebook.com/v19.0"

def upload_to_instagram(video_path: str, title: str, hashtags: str) -> str:
    """
    Upload a Reel to Instagram via Graph API.
    NOTE: Instagram requires the video to be publicly accessible via URL.
    We use a free transfer.sh upload to get a temporary public URL.
    """

    # ── 1. Get a public URL for the file via transfer.sh ─────
    print("  Getting public URL for Instagram upload …")
    filename = video_path.split("/")[-1]
    with open(video_path, "rb") as f:
        r = requests.put(f"https://transfer.sh/{filename}", data=f, timeout=120)
    r.raise_for_status()
    public_url = r.text.strip()
    print(f"  Public URL: {public_url}")

    caption = f"{title}\n\n{hashtags}\n\n#reels #shorts"

    # ── 2. Create media container ─────────────────────────────
    print("  Creating Instagram media container …")
    r = requests.post(
        f"{BASE}/{INSTAGRAM_USER_ID}/media",
        params={
            "media_type": "REELS",
            "video_url": public_url,
            "caption": caption[:2200],
            "share_to_feed": "true",
            "access_token": INSTAGRAM_TOKEN,
        },
        timeout=30
    )
    r.raise_for_status()
    container_id = r.json()["id"]
    print(f"  Container ID: {container_id}")

    # ── 3. Wait for processing ────────────────────────────────
    print("  Waiting for Instagram to process video …")
    for attempt in range(20):
        time.sleep(15)
        status_r = requests.get(
            f"{BASE}/{container_id}",
            params={"fields": "status_code", "access_token": INSTAGRAM_TOKEN},
            timeout=15
        )
        status = status_r.json().get("status_code", "")
        print(f"  Status: {status} (attempt {attempt+1})")
        if status == "FINISHED":
            break
        if status == "ERROR":
            raise RuntimeError("Instagram rejected the video. Check format/codec.")
    else:
        raise TimeoutError("Instagram processing timed out after 5 minutes.")

    # ── 4. Publish ────────────────────────────────────────────
    print("  Publishing Reel …")
    pub_r = requests.post(
        f"{BASE}/{INSTAGRAM_USER_ID}/media_publish",
        params={"creation_id": container_id, "access_token": INSTAGRAM_TOKEN},
        timeout=30
    )
    pub_r.raise_for_status()
    media_id = pub_r.json()["id"]

    # get permalink
    link_r = requests.get(
        f"{BASE}/{media_id}",
        params={"fields": "permalink", "access_token": INSTAGRAM_TOKEN},
        timeout=15
    )
    url = link_r.json().get("permalink", f"https://instagram.com/p/{media_id}")
    print(f"  Instagram URL: {url}")
    return url
