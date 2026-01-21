# FORMATR

**Neo-Brutalist. Local-First. Universal Converter.**

FORMATR is a powerful, privacy-focused desktop file converter with a bold, tactile UI. No clouds. No tracking. Pure utility.

![FORMATR Screenshot](https://via.placeholder.com/800x400?text=FORMATR+UI+Placeholder)

## 📥 Download

### **[Windows Standalone (.exe)](../../releases)**
The easiest way to use FORMATR. No installation required.
1.  Go to the **[Releases](../../releases)** page on the right.
2.  Download the latest `FORMATR_Windows.zip`.
3.  Unzip and run `FORMATR.exe`.

---

## ⚡ Features
*   **🎨 Images**: Resize (Slider/%), Compress, Convert (PNG, JPG, WEBP, PDF).
*   **📄 Documents**: 
    *   **PDF Tools**: Compress PDF (Quality Slider), PDF to Images.
    *   **Cross-Convert**: Image → PDF/DOCX and DOCX/PDF → Image.
*   **🎥 Audio/Video**: Convert MP3, WAV, MP4, MKV, etc. (Requires FFmpeg).
*   **🌑 Dark Mode**: High-contrast Yellow/Black/Red theme.
*   **🔒 Privacy**: All processing happens **locally** on your machine.

## 🛠️ Requirements (For Source Run)
If you are running from source (Python):
*   **Python 3.10+**
*   **FFmpeg**: Required for Audio/Video conversion.
*   **Microsoft Word** (or LibreOffice): Required for DOCX to PDF conversion.

## 💻 Run from Source
1.  Clone the repo.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    python run_app.py
    ```

## 📦 Build Instructions
To build your own `.exe`:
1.  Install PyInstaller: `pip install pyinstaller`
2.  Run the build command:
    ```bash
    python -m PyInstaller --noconfirm --onedir --windowed --name "FORMATR" --icon "frontend/logo.png" --add-data "frontend;frontend" --add-data "backend;backend" --hidden-import "uvicorn" --hidden-import "uvicorn.logging" --hidden-import "uvicorn.loops" --hidden-import "uvicorn.loops.auto" --hidden-import "uvicorn.protocols" --hidden-import "uvicorn.protocols.http" --hidden-import "uvicorn.protocols.http.auto" --hidden-import "uvicorn.lifespan" --hidden-import "uvicorn.lifespan.on" --hidden-import "engineio.async_drivers.threading" run_app.py
    ```
3.  Result is in `dist/FORMATR`.

## License
MIT
