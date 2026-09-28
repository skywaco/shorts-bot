"""
requeue.py — Find and upload any missed videos
Run this anytime you think a video was missed.

Usage:
    python requeue.py           — shows all unuploaded videos and queues them
    python requeue.py --upload  — queues AND immediately uploads them
"""

import os
import json
import sys
from datetime import datetime
from openpyxl import load_workbook
from config import LOG_FILE, PENDING_FILE, OUTPUT_DIR

def get_uploaded_files() -> set:
    """Read Excel tracker and return set of video files already uploaded."""
    uploaded = set()
    if not os.path.exists(LOG_FILE):
        return uploaded
    try:
        wb = load_workbook(LOG_FILE)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, values_only=True):
            video_file = row[9]   # column J = video file path
            status = row[10]      # column K = status
            yt_url = row[7]       # column H = YouTube URL
            if video_file and status == "uploaded" and yt_url and yt_url != "pending":
                uploaded.add(str(video_file))
    except Exception as e:
        print(f"  Warning: could not read Excel: {e}")
    return uploaded

def get_all_videos() -> list:
    """Get all MP4 files in videos folder sorted by date."""
    if not os.path.exists(OUTPUT_DIR):
        return []
    files = []
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".mp4"):
            full_path = os.path.abspath(os.path.join(OUTPUT_DIR, f))
            files.append(full_path)
    files.sort()
    return files

def get_video_info_from_excel(video_file: str) -> dict:
    """Try to get title and hashtags from Excel for a given video file."""
    if not os.path.exists(LOG_FILE):
        return {}
    try:
        wb = load_workbook(LOG_FILE)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[9] and str(row[9]) == video_file:
                return {
                    "topic": str(row[3] or ""),
                    "title": str(row[4] or ""),
                    "hashtags": str(row[6] or "#shorts #viral #facts #trending"),
                    "script": "",
                }
    except Exception:
        pass
    return {}

def main():
    auto_upload = "--upload" in sys.argv

    print("\n🔍  REQUEUE TOOL — Finding missed videos")
    print(f"    {datetime.now().strftime('%A %d %B %Y, %H:%M')}\n")

    all_videos = get_all_videos()
    uploaded = get_uploaded_files()

    if not all_videos:
        print("  No videos found in videos/ folder.")
        return

    missed = [v for v in all_videos if v not in uploaded]

    print(f"  Total videos on disk : {len(all_videos)}")
    print(f"  Already uploaded     : {len(uploaded)}")
    print(f"  Missed / not uploaded: {len(missed)}\n")

    if not missed:
        print("  All videos have been uploaded. Nothing to do!")
        return

    print("  Missed videos:")
    for i, v in enumerate(missed):
        fname = os.path.basename(v)
        print(f"    {i+1}. {fname}")

    print()

    # build queue
    queue = []
    for v in missed:
        info = get_video_info_from_excel(v)
        fname = os.path.basename(v)
        # extract date from filename for display
        queue.append({
            "topic":      info.get("topic") or fname,
            "title":      info.get("title") or fname.replace(".mp4", "").replace("_", " "),
            "hashtags":   info.get("hashtags") or "#shorts #viral #facts #trending",
            "script":     "",
            "video_file": v,
            "status":     "created",
            "yt_url":     "",
            "ig_url":     "",
        })

    # save to pending
    os.makedirs(os.path.dirname(PENDING_FILE), exist_ok=True)
    with open(PENDING_FILE, "w") as f:
        json.dump(queue, f, indent=2)

    print(f"  Queued {len(queue)} video(s) in pending.json")

    if auto_upload:
        print("\n  Starting upload now...\n")
        from upload_videos import main as upload_main
        upload_main()
    else:
        print("\n  To upload them now run:")
        print("  python upload_videos.py")
        print("\n  Or to queue AND upload in one command:")
        print("  python requeue.py --upload")

if __name__ == "__main__":
    main()
