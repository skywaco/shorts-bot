import asyncio
import edge_tts
import os
from mutagen.mp3 import MP3

# Voice options — will try each one until one works
VOICES = [
    "en-US-AndrewNeural",
    "en-US-GuyNeural",
    "en-US-AriaNeural",
    "en-US-JennyNeural",
]

async def _synthesize_one(text: str, path: str):
    """Try multiple voices until one works."""
    for voice in VOICES:
        try:
            communicate = edge_tts.Communicate(
                text, voice, rate="-18%", pitch="+2Hz", volume="+10%"
            )
            await communicate.save(path)
            # verify file was created and has content
            if os.path.exists(path) and os.path.getsize(path) > 1000:
                return
        except Exception as e:
            print(f"    Voice {voice} failed: {e}, trying next...")
            continue
    raise RuntimeError(f"All voices failed for text: {text[:50]}")

async def _synthesize_all(sentences: list, output_dir: str) -> list:
    paths = []
    for i, sentence in enumerate(sentences):
        text = sentence.get("text", "")
        # clean text — remove any special chars that break TTS
        text = ''.join(c for c in text if ord(c) < 8000)
        text = text.strip()
        if not text:
            text = "And that is a fact worth knowing today."
        path = os.path.join(output_dir, f"sentence_{i}.mp3")
        await _synthesize_one(text, path)
        paths.append(path)
    return paths

def get_sentence_durations(sentence_audio_paths: list) -> list:
    durations = []
    for path in sentence_audio_paths:
        try:
            duration = MP3(path).info.length
        except Exception:
            duration = 4.0
        durations.append(duration)
    return durations

def generate_voiceover(script: str, output_path: str, voice: str = VOICES[0]):
    print(f"  Generating voiceover ...")
    async def run():
        await _synthesize_one(script, output_path)
    asyncio.run(run())
    print(f"  Voiceover done.")

def generate_sentence_voiceovers(sentences: list, output_dir: str, voice: str = VOICES[0]) -> tuple:
    print(f"  Generating synced voiceovers ...")
    os.makedirs(output_dir, exist_ok=True)
    paths = asyncio.run(_synthesize_all(sentences, output_dir))
    durations = get_sentence_durations(paths)
    total = sum(durations)
    print(f"  {len(paths)} audio files, total: {total:.1f}s")
    return paths, durations
