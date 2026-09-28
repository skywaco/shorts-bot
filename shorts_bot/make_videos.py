"""
make_videos.py — Runs every night at 10 PM
Creates 2 viral Shorts with matched footage + synced voice + karaoke captions + music.
"""

import os
import json
import shutil
import tempfile
from datetime import datetime

from config import OUTPUT_DIR, PENDING_FILE
from generate_script import generate_script
from generate_voiceover import generate_sentence_voiceovers
from fetch_footage import fetch_matched_clips
from assemble_video import assemble_video
from excel_logger import log_video

def make_one_video(index: int) -> dict:
    print(f"\n{'='*50}")
    print(f"  VIDEO {index+1} / 2")
    print(f"{'='*50}")

    # 1. Generate script
    print("\n[1/4] Generating script ...")
    data = generate_script()
    sentences = data.get("sentences", [])

    tmp_dir = tempfile.mkdtemp()

    # 2. Generate one voiceover per sentence (for perfect sync)
    print("\n[2/4] Generating synced voiceovers ...")
    audio_dir = os.path.join(tmp_dir, "audio")
    sentence_paths, sentence_durations = generate_sentence_voiceovers(sentences, audio_dir)

    # 3. Fetch one matching clip per sentence
    print(f"\n[3/4] Fetching matched footage ...")
    clip_folder = os.path.join(tmp_dir, "clips")
    clips = fetch_matched_clips(sentences, clip_folder)

    # if fewer clips than sentences, duplicate last clip
    while len(clips) < len(sentences):
        clips.append(clips[-1] if clips else None)
    clips = [c for c in clips if c]

    if not clips:
        raise RuntimeError("No clips downloaded")

    # align counts
    min_count = min(len(clips), len(sentences), len(sentence_paths))
    clips = clips[:min_count]
    sentences = sentences[:min_count]
    sentence_paths = sentence_paths[:min_count]
    sentence_durations = sentence_durations[:min_count]

    # 4. Assemble video
    print("\n[4/4] Assembling video ...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"short_{timestamp}_{index+1}.mp4")

    assemble_video(
        clips=clips,
        audio_path=sentence_paths[0],  # placeholder, combined inside
        output_path=output_path,
        title=data["title"],
        script=data["script"],
        sentences=sentences,
        sentence_audio_paths=sentence_paths,
        sentence_durations=sentence_durations
    )

    shutil.rmtree(tmp_dir, ignore_errors=True)

    entry = {
        "topic":      data["topic"],
        "title":      data["title"],
        "hashtags":   data["hashtags"],
        "script":     data["script"],
        "video_file": os.path.abspath(output_path),
        "status":     "created",
        "yt_url":     "",
        "ig_url":     "",
    }
    log_video(entry)
    return entry


def main():
    print("\n🎬  SHORTS BOT — VIDEO CREATION MODE")
    print(f"    {datetime.now().strftime('%A %d %B %Y, %H:%M')}\n")

    pending = []
    for i in range(2):
        try:
            entry = make_one_video(i)
            pending.append(entry)
            print(f"\n  ✅  Video {i+1} complete: {entry['video_file']}")
        except Exception as e:
            import traceback
            print(f"\n  ❌  Video {i+1} failed: {e}")
            traceback.print_exc()

    os.makedirs(os.path.dirname(PENDING_FILE), exist_ok=True)
    with open(PENDING_FILE, "w") as f:
        json.dump(pending, f, indent=2)

    print(f"\n{'='*50}")
    print(f"  Done! {len(pending)} video(s) saved and queued.")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
