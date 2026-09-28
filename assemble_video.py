import subprocess
import os
import requests
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS

FONT_PATH = "assets/font.ttf"
MUSIC_PATH = "assets/bgmusic.mp3"

MUSIC_URLS = [
    "https://cdn.pixabay.com/download/audio/2022/10/25/audio_946ff6c3f0.mp3",
    "https://cdn.pixabay.com/download/audio/2022/08/02/audio_884fe92c21.mp3",
    "https://cdn.pixabay.com/download/audio/2021/11/13/audio_cb4f5b9836.mp3",
    "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0c6ff1bab.mp3",
]

def ensure_music() -> bool:
    if os.path.exists(MUSIC_PATH) and os.path.getsize(MUSIC_PATH) > 10000:
        return True
    os.makedirs("assets", exist_ok=True)
    for url in MUSIC_URLS:
        try:
            print("  Downloading background music ...")
            r = requests.get(url, timeout=20)
            if r.ok and len(r.content) > 10000:
                with open(MUSIC_PATH, "wb") as f:
                    f.write(r.content)
                print("  Music downloaded.")
                return True
        except Exception:
            continue
    print("  Music unavailable.")
    return False

def safe_text(text: str) -> str:
    result = ""
    for c in text:
        if ord(c) > 7999:
            continue
        if c in ("'", '"', "\\", "%", "[", "]", "<", ">", ";"):
            continue
        if c == ":":
            result += "-"
        elif c == "&":
            result += "and"
        else:
            result += c
    return result.strip()

def concat_audio_files(audio_paths: list, output_path: str):
    list_file = output_path + "_list.txt"
    with open(list_file, "w") as f:
        for p in audio_paths:
            abs_path = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")
    cmd = ["C:\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-f", "concat", "-safe", "0",
           "-i", list_file, "-c", "copy", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(list_file)
    if result.returncode != 0:
        raise RuntimeError(f"Audio concat failed: {result.stderr[-500:]}")

def assemble_video(clips: list, audio_path: str, output_path: str,
                   title: str, script: str, sentences: list = None,
                   sentence_audio_paths: list = None, sentence_durations: list = None):

    n = len(clips)
    if n == 0:
        raise RuntimeError("No clips available")

    has_music = ensure_music()

    if sentence_durations and len(sentence_durations) == n:
        clip_durations = sentence_durations
        total_duration = sum(clip_durations)
    else:
        from mutagen.mp3 import MP3
        total_duration = MP3(audio_path).info.length
        clip_durations = [total_duration / n] * n

    print(f"  Total duration: {total_duration:.1f}s")

    if sentence_audio_paths and len(sentence_audio_paths) == n:
        combined_audio = audio_path + "_combined.mp3"
        concat_audio_files(sentence_audio_paths, combined_audio)
        final_audio = combined_audio
    else:
        final_audio = audio_path

    # ── FFmpeg inputs ─────────────────────────────────────────
    input_args = []
    for clip, dur in zip(clips, clip_durations):
        input_args += ["-stream_loop", "-1", "-t", f"{dur:.3f}", "-i", clip]
    input_args += ["-i", final_audio]
    audio_index = n

    if has_music and os.path.exists(MUSIC_PATH):
        input_args += ["-stream_loop", "-1", "-i", MUSIC_PATH]
        music_index = n + 1
    else:
        music_index = None

    # ── Scale each clip to exact 1080x1920 ───────────────────
    scale = (
        f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}"
        f":force_original_aspect_ratio=increase,"
        f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT}:exact=1,"
        f"setsar=1,fps={FPS}"
    )

    parts = []
    for i in range(n):
        parts.append(f"[{i}:v]{scale}[v{i}]")

    concat_in = "".join(f"[v{i}]" for i in range(n))
    parts.append(f"{concat_in}concat=n={n}:v=1:a=0[vconcat]")
    parts.append(f"[vconcat]trim=duration={total_duration:.3f},setpts=PTS-STARTPTS[vtrim]")

    # ── Title bar at top only — no black box on captions ─────
    safe_title = safe_text(title)[:40]
    parts.append(
        f"[vtrim]"
        f"drawbox=x=0:y=0:w={VIDEO_WIDTH}:h=110:color=black@0.8:t=fill,"
        f"drawtext=fontfile='{FONT_PATH}'"
        f":text='{safe_title}'"
        f":fontcolor=white"
        f":fontsize=48"
        f":x=(w-text_w)/2"
        f":y=38"
        f":borderw=3"
        f":bordercolor=black"
        f"[vtitle]"
    )

    # ── TikTok style captions — 2 lines, white + red last word ─
    # Line 1 sits at y = VIDEO_HEIGHT - 200
    # Line 2 sits at y = VIDEO_HEIGHT - 120
    # No black background box — text only with thick border

    LINE1_Y = VIDEO_HEIGHT - 320   # 1600
    LINE2_Y = VIDEO_HEIGHT - 230   # 1690
    FONT_SIZE = 60
    BORDER = 5

    if sentences and len(sentences) == n:
        current = "[vtitle]"
        t = 0.0

        for i, (sent, dur) in enumerate(zip(sentences, clip_durations)):
            raw = safe_text(sent.get("text", "")).upper()
            words = raw.split()
            t_start = t
            t_end = t + dur

            # split words into line1 and line2
            if len(words) <= 2:
                line1 = ""
                line2 = " ".join(words)
                last = ""
            else:
                mid = len(words) // 2
                line1 = " ".join(words[:mid])
                line2 = " ".join(words[mid:-1])
                last = words[-1]  # last word goes red on line2

            # we build up to 3 drawtext layers per sentence
            labels = []
            filters_this = []

            # layer A — line 1 white
            if line1:
                la = f"[cap{i}a]"
                filters_this.append(
                    f"drawtext=fontfile='{FONT_PATH}'"
                    f":text='{line1}'"
                    f":fontcolor=white"
                    f":fontsize={FONT_SIZE}"
                    f":x=(w-text_w)/2"
                    f":y={LINE1_Y}"
                    f":borderw={BORDER}"
                    f":bordercolor=black"
                    f":enable='between(t,{t_start:.3f},{t_end:.3f})'"
                )
                labels.append(la)

            # layer B — line 2 white (without last word)
            if line2:
                lb = f"[cap{i}b]"
                filters_this.append(
                    f"drawtext=fontfile='{FONT_PATH}'"
                    f":text='{line2}'"
                    f":fontcolor=white"
                    f":fontsize={FONT_SIZE}"
                    f":x=(w-text_w)/2"
                    f":y={LINE2_Y}"
                    f":borderw={BORDER}"
                    f":bordercolor=black"
                    f":enable='between(t,{t_start:.3f},{t_end:.3f})'"
                )
                labels.append(lb)

            # layer C — last word appended to line2 in red
            # merge line2 + last into one centered line
            # white part = line2, red part = last word on new line
            if last:
                lc = f"[cap{i}c]"
                filters_this.append(
                    f"drawtext=fontfile='{FONT_PATH}'"
                    f":text='{last}'"
                    f":fontcolor=red"
                    f":fontsize={FONT_SIZE}"
                    f":x=(w-text_w)/2"
                    f":y={LINE2_Y + 70}"
                    f":borderw={BORDER}"
                    f":bordercolor=black"
                    f":enable='between(t,{t_start:.3f},{t_end:.3f})'"
                )
                labels.append(lc)

            # chain all layers for this sentence
            out = f"[vc{i}]" if i < n - 1 else "[vfinal]"
            if not filters_this:
                # no caption for this sentence, just pass through
                parts.append(f"{current}null{out}")
            else:
                chain = ",".join(filters_this)
                parts.append(f"{current}{chain}{out}")
            current = out
            t += dur

        final_video = "[vfinal]"
    else:
        final_video = "[vtitle]"

    filtergraph = ";".join(parts)

    # audio mix
    if music_index is not None:
        filtergraph += (
            f";[{audio_index}:a]volume=1.0[voice]"
            f";[{music_index}:a]volume=0.07,atrim=duration={total_duration:.3f}[music]"
            f";[voice][music]amix=inputs=2:duration=first[aout]"
        )
        audio_map = "[aout]"
    else:
        audio_map = f"{audio_index}:a"

    cmd = [
        "C:\\ffmpeg\\bin\\ffmpeg.exe", "-y",
        *input_args,
        "-filter_complex", filtergraph,
        "-map", final_video,
        "-map", audio_map,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        output_path
    ]

    print("  Running FFmpeg ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg error:\n", result.stderr[-3000:])
        raise RuntimeError("FFmpeg failed")
    print(f"  Video saved -> {output_path}")
