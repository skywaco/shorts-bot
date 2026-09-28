# 🎬 Shorts Bot — Complete Setup Guide
Zero cost. Fully automated. YouTube + Instagram.

---

## How It Works

```
Every night 10 PM          Every morning 8 AM
─────────────────          ──────────────────
make_videos.py             upload_videos.py
  │                          │
  ├─ Claude → topic+script   ├─ Upload to YouTube
  ├─ Edge TTS → voiceover    ├─ Upload to Instagram
  ├─ Pexels → footage        └─ Update Excel log
  └─ FFmpeg → 2 MP4 files
```

---

## STEP 1 — Install Prerequisites

### Python
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or newer
3. ✅ CHECK "Add Python to PATH" during install

### FFmpeg
1. Go to https://www.gyan.dev/ffmpeg/builds/
2. Download **ffmpeg-release-essentials.zip**
3. Extract to `C:\ffmpeg`
4. Press Win+S → search "environment variables"
5. Click "Environment Variables" → under System Variables find "Path"
6. Click Edit → New → type `C:\ffmpeg\bin` → OK all the way

---

## STEP 2 — Get Your Free API Keys

### Anthropic (Claude) — FREE daily credits
1. Go to https://console.anthropic.com
2. Sign up → API Keys → Create Key
3. Copy and paste into `config.py` → `ANTHROPIC_API_KEY`

### Pexels — FREE unlimited
1. Go to https://www.pexels.com/api/
2. Sign up → your API key appears on the page
3. Copy and paste into `config.py` → `PEXELS_API_KEY`

### YouTube — FREE (Google account needed)
1. Go to https://console.cloud.google.com
2. Click "New Project" → name it "ShortsBot" → Create
3. Search for "YouTube Data API v3" → Enable
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Application type: **Desktop App** → name it "ShortsBot" → Create
6. Click the download icon (⬇️) next to your new credential
7. Rename the downloaded file to **client_secrets.json**
8. Put it in your `shorts_bot` folder

### Instagram — FREE (Business/Creator account needed)
1. Make sure your Instagram is a Professional account
   (Instagram app → Settings → Account → Switch to Professional)
2. Go to https://developers.facebook.com
3. Create App → type: **Business**
4. Add Product: **Instagram Graph API**
5. Under Instagram Graph API → Generate Token → connect your account
6. Copy the token → paste into `config.py` → `INSTAGRAM_TOKEN`
7. To get your User ID: visit
   `https://graph.facebook.com/me?fields=id&access_token=YOUR_TOKEN`
8. Copy the "id" number → paste into `config.py` → `INSTAGRAM_USER_ID`

---

## STEP 3 — Setup the Bot

1. Copy the entire `shorts_bot` folder to `C:\Users\naikh\shorts_bot`
2. Open `config.py` and fill in all 5 keys
3. Double-click `setup.bat` — this installs all packages automatically
4. Wait for it to finish — it says "Setup complete!" when done

---

## STEP 4 — Test It Manually First

Open Command Prompt in your `shorts_bot` folder:
```
cd C:\Users\naikh\shorts_bot
python make_videos.py
```

First run: a browser window will open asking you to log into Google.
Log in and allow access. This only happens once — it saves a token.

Watch the terminal. It will:
- Generate 2 topics and scripts
- Create voiceovers
- Download footage
- Build 2 MP4 files in the `videos/` folder
- Create `logs/tracker.xlsx`

Then test upload:
```
python upload_videos.py
```

---

## STEP 5 — Schedule Automatically (Task Scheduler)

### Schedule video creation (10 PM every night):
1. Press Win+S → search "Task Scheduler" → Open
2. Click "Import Task…" on the right panel
3. Browse to your shorts_bot folder → select `task_make_videos.xml`
4. Click OK → task is now scheduled

### Schedule video upload (8 AM every morning):
1. In Task Scheduler → click "Import Task…" again
2. Browse to your shorts_bot folder → select `task_upload_videos.xml`
3. Click OK → task is now scheduled

That's it! Your PC will:
- Generate 2 videos every night at 10 PM
- Upload both to YouTube + Instagram every morning at 8 AM
- Log everything to `logs/tracker.xlsx`

---

## Your Excel Tracker

Opens at: `shorts_bot/logs/tracker.xlsx`

Columns:
| Column | What it tracks |
|--------|---------------|
| Date / Time | When video was made |
| Video # | Sequential number |
| Topic | What the video is about |
| Title | The actual video title |
| Script preview | First 120 chars of script |
| Hashtags | All hashtags used |
| YouTube URL | Clickable link |
| Instagram URL | Clickable link |
| Video File | Local file path |
| Status | created → uploaded |

---

## Troubleshooting

**"FFmpeg not found"** → Make sure `C:\ffmpeg\bin` is in your PATH (Step 1)

**"Module not found"** → Run `setup.bat` again

**YouTube browser window won't open** → Run `python upload_videos.py` manually from Command Prompt

**Instagram upload fails** → Check your token hasn't expired (refresh every 60 days at developers.facebook.com)

**Videos look bad** → Edit `config.py` → lower `CRF` value in `assemble_video.py` (18 = best quality, 28 = smaller file)

---

## File Structure

```
shorts_bot/
├── config.py              ← YOUR KEYS GO HERE
├── make_videos.py         ← Day 1: creates videos
├── upload_videos.py       ← Day 2: uploads videos
├── generate_script.py     ← Claude AI topic+script
├── generate_voiceover.py  ← Edge TTS voice
├── fetch_footage.py       ← Pexels stock footage
├── assemble_video.py      ← FFmpeg video builder
├── upload_youtube.py      ← YouTube uploader
├── upload_instagram.py    ← Instagram uploader
├── excel_logger.py        ← Excel tracker
├── setup.bat              ← Run once to install
├── task_make_videos.xml   ← Import into Task Scheduler
├── task_upload_videos.xml ← Import into Task Scheduler
├── client_secrets.json    ← Download from Google Cloud
├── assets/
│   └── font.ttf           ← Caption font (auto-downloaded)
├── videos/                ← Your MP4 files go here
└── logs/
    ├── tracker.xlsx        ← Your Excel dashboard
    ├── pending.json        ← Queue between make & upload
    └── youtube_token.pickle← Saved Google login (auto)
```
