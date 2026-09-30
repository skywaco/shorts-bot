@echo off
echo.
echo  ==========================================
echo   SHORTS BOT — FIRST TIME SETUP
echo  ==========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found.
    echo  Download from: https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install!
    pause
    exit /b 1
)
echo  [OK] Python found

:: Check FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: FFmpeg not found.
    echo  1. Download from: https://www.gyan.dev/ffmpeg/builds/
    echo     Click "ffmpeg-release-essentials.zip"
    echo  2. Extract to C:\ffmpeg
    echo  3. Add C:\ffmpeg\bin to your System PATH
    echo  4. Re-run this setup
    echo.
    pause
    exit /b 1
)
echo  [OK] FFmpeg found

:: Install Python packages
echo.
echo  Installing Python packages...
pip install google-generativeai edge-tts requests mutagen openpyxl ^
    google-api-python-client google-auth-oauthlib ^
    google-auth-httplib2 -q

echo  [OK] Packages installed

:: Download a clean font for captions
echo.
echo  Downloading caption font...
mkdir assets 2>nul
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Bold.ttf' -OutFile 'assets\font.ttf'" 2>nul
if exist assets\font.ttf (
    echo  [OK] Font downloaded
) else (
    echo  [WARN] Font download failed. Copy any .ttf font to assets\font.ttf manually.
)

:: Create logs and videos folder
mkdir logs 2>nul
mkdir videos 2>nul
echo  [OK] Folders created

echo.
echo  ==========================================
echo   Setup complete!
echo.
echo   NEXT STEPS:
echo   1. Open config.py and fill in your API keys
echo   2. Put client_secrets.json in this folder
echo   3. Run:  python make_videos.py
echo  ==========================================
echo.
pause
