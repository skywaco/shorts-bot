import requests
import os
import random
import time
from config import PEXELS_API_KEY

HEADERS = {"Authorization": PEXELS_API_KEY}

def search_clips_for_keyword(keyword: str, count: int = 6) -> list:
    """
    Search Pexels with keyword. Tries portrait first then landscape.
    Returns list of unique download URLs.
    """
    links = []
    seen_ids = set()

    for orientation in ["portrait", None]:
        if len(links) >= count:
            break
        params = {
            "query": keyword,
            "size": "medium",
            "per_page": 15,
        }
        if orientation:
            params["orientation"] = orientation
        try:
            r = requests.get(
                "https://api.pexels.com/videos/search",
                headers=HEADERS, params=params, timeout=15
            )
            if not r.ok:
                continue
            videos = r.json().get("videos", [])
            for v in videos:
                vid_id = v.get("id")
                if vid_id in seen_ids:
                    continue
                seen_ids.add(vid_id)
                # prefer HD portrait files
                files = sorted(
                    v["video_files"],
                    key=lambda f: (
                        1 if f.get("height", 0) > f.get("width", 0) else 0,
                        f.get("width", 0)
                    ),
                    reverse=True
                )
                for f in files:
                    if f.get("link") and f["link"] not in links:
                        links.append(f["link"])
                        break
        except Exception as e:
            print(f"    Search error: {e}")
            continue

    random.shuffle(links)
    return links[:count]

def download_clip(link: str, path: str) -> bool:
    """Download a single clip with 3 retries."""
    for attempt in range(3):
        try:
            with requests.get(link, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 64):
                        f.write(chunk)
            # verify file size
            if os.path.getsize(path) > 10000:
                return True
        except Exception as e:
            print(f"    Retry {attempt+1}/3: {e}")
            time.sleep(2)
    return False

def fetch_matched_clips(sentences: list, folder: str) -> list:
    """
    Fetch one unique clip per sentence using its specific keyword.
    Falls back to broader search if no match found.
    Never reuses same clip twice.
    """
    os.makedirs(folder, exist_ok=True)
    paths = []
    used_links = set()

    for i, sentence in enumerate(sentences):
        keyword = sentence.get("keyword", "nature landscape")
        print(f"  Clip {i+1}/{len(sentences)}: '{keyword}' ...")

        # try exact keyword first
        candidates = search_clips_for_keyword(keyword, count=8)
        fresh = [l for l in candidates if l not in used_links]

        # if no fresh — try first 2 words of keyword (broader)
        if not fresh and len(keyword.split()) > 2:
            broad = " ".join(keyword.split()[:2])
            print(f"    Broadening to: '{broad}'")
            candidates = search_clips_for_keyword(broad, count=8)
            fresh = [l for l in candidates if l not in used_links]

        # final fallback — generic but relevant
        if not fresh:
            fallbacks = [
                "people working office", "city street walking",
                "nature landscape aerial", "technology computer screen",
                "person thinking closeup", "ocean waves beach"
            ]
            for fb in fallbacks:
                candidates = search_clips_for_keyword(fb, count=6)
                fresh = [l for l in candidates if l not in used_links]
                if fresh:
                    print(f"    Using fallback: '{fb}'")
                    break

        if not fresh:
            print(f"    No unique clip found — skipping")
            continue

        link = fresh[0]
        used_links.add(link)
        path = os.path.join(folder, f"clip_{i}.mp4")

        if download_clip(link, path):
            paths.append(path)
            print(f"    Downloaded")
        else:
            print(f"    Download failed")

    return paths

def search_videos(keyword: str, count: int = 8) -> list:
    return search_clips_for_keyword(keyword, count)

def download_clips(links: list, folder: str, prefix: str = "clip") -> list:
    os.makedirs(folder, exist_ok=True)
    paths = []
    for i, link in enumerate(links):
        path = os.path.join(folder, f"{prefix}_{i}.mp4")
        print(f"  Downloading clip {i+1}/{len(links)} ...")
        if download_clip(link, path):
            paths.append(path)
    return paths
