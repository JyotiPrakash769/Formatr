# FORMATR

A local-first, offline, privacy-focused file converter.
Illustrative / Hand-Drawn design. No clouds. No tracking. Pure utility.

## Features
- **Images**: PNG, JPG, WEBP (Convert, Compress, Resize)
- **Docs**: PDF to Images, Doc to PDF
- **Audio**: MP3, WAV, OGG
- **Video**: MP4, MKV, AVI

## Requirements
- **Python 3.10+**
- **FFmpeg**: Must be in your system PATH for Audio/Video tools.
- **LibreOffice**: Must be installed for Document tools.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python run_app.py
   ```

## Building for Windows
To create a standalone `.exe`:
```bash
python build_app.py
```
The executable will be in `dist/FORMATR/FORMATR.exe`.

## Architecture
- **Backend**: FastAPI (Localhost server)
- **Frontend**: HTML/CSS/JS (Illustrative UI)
- **Shell**: PySide6 (QtWebEngine)

## License
MIT
