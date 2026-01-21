import os
import requests
import zipfile
import io
import shutil

FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
BIN_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "bin")

def download_ffmpeg():
    if os.path.exists(os.path.join(BIN_DIR, "ffmpeg.exe")):
        print("FFmpeg already exists. Skipping download.")
        return

    print("Downloading FFmpeg (this may take a while)...")
    try:
        response = requests.get(FFMPEG_URL)
        response.raise_for_status()
        
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            # Flatten structure: find the bin folder in zip and extract to our BIN_DIR
            for file in z.namelist():
                if file.endswith("bin/ffmpeg.exe") or file.endswith("bin/ffprobe.exe"):
                    filename = os.path.basename(file)
                    target_path = os.path.join(BIN_DIR, filename)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    
                    with open(target_path, "wb") as f:
                        f.write(z.read(file))
                        
        print(f"FFmpeg downloaded to {BIN_DIR}")
    except Exception as e:
        print(f"Failed to download FFmpeg: {e}")

if __name__ == "__main__":
    download_ffmpeg()
