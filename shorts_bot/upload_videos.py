"""
upload_videos.py  ── Run this TOMORROW (Day 2)
───────────────────────────────────────────────
Reads the pending queue, uploads both videos to YouTube Shorts
and Instagram Reels, then updates the Excel log with URLs.

Schedule: Task Scheduler → runs next day at 8 AM
"""

import json
import os
from datetime import datetime

from config import PENDING_FILE
from upload_youtube import upload_to_youtube
from upload_instagram import upload_to_instagram
from excel_logger import update_urls


def main():
    print("\n🚀  SHORTS BOT — UPLOAD MODE")
    print(f"    {datetime.now().strftime('%A %d %B %Y, %H:%M')}\n")

    if not os.path.exists(PENDING_FILE):
        print("  No pending videos found. Run make_videos.py first.")
        return

    with open(PENDING_FILE) as f:
        pending = json.load(f)

    if not pending:
        print("  Pending queue is empty.")
        return

    print(f"  Found {len(pending)} video(s) to upload.\n")

    for i, entry in enumerate(pending):
        video_file = entry["video_file"]
        title      = entry["title"]
        hashtags   = entry["hashtags"]
        topic      = entry["topic"]

        print(f"\n{'='*50}")
        print(f"  UPLOADING VIDEO {i+1}: {title}")
        print(f"{'='*50}")

        if not os.path.exists(video_file):
            print(f"  ❌ File not found: {video_file}")
            continue

        yt_url = ""
        ig_url = ""

        # ── YouTube ─────────────────────────────────────────
        try:
            description = (
                f"🎯 {topic}\n\n"
                f"Watch till the end!\n\n"
                f"Subscribe for daily facts & tips!"
            )
            yt_url = upload_to_youtube(video_file, title, description, hashtags)
            print(f"  ✅ YouTube: {yt_url}")
        except Exception as e:
            print(f"  ❌ YouTube upload failed: {e}")

        # ── Instagram ────────────────────────────────────────
        try:
            ig_url = upload_to_instagram(video_file, title, hashtags)
            print(f"  ✅ Instagram: {ig_url}")
        except Exception as e:
            print(f"  ❌ Instagram upload failed: {e}")

        # ── Update Excel ─────────────────────────────────────
        update_urls(video_file, yt_url=yt_url, ig_url=ig_url)

    # Clear pending queue after upload
    with open(PENDING_FILE, "w") as f:
        json.dump([], f)

    print(f"\n{'='*50}")
    print(f"  All uploads complete! Check logs/tracker.xlsx")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
