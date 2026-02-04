import os
import subprocess
import shutil
import sys

def build():
    # Ensure FFmpeg is present
    from utils.download_ffmpeg import download_ffmpeg
    download_ffmpeg()

    # PyInstaller arguments
    args = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--name=FORMATR",
        "--windowed", 
        "--add-data=frontend;frontend",
        "--add-data=backend/bin;backend/bin", # Bundle FFmpeg
        # Important hidden imports for FastAPI/Uvicorn
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=uvicorn.lifespan.off",
        "--hidden-import=fastapi",
        "--hidden-import=pyside6",
        "--hidden-import=markdown",
        "--hidden-import=yaml",
        "--hidden-import=xmltodict",
        "--hidden-import=xhtml2pdf",
        "--hidden-import=reportlab.graphics.barcode.code128",
        "--hidden-import=reportlab.graphics.barcode.code39",
        "--hidden-import=reportlab.graphics.barcode.usps",
        # Phase 1 hidden imports
        "--hidden-import=openpyxl",
        "--hidden-import=bs4",
        "--hidden-import=jsbeautifier",
        "--hidden-import=cssbeautifier",
        # Phase 2 Tier 1 hidden imports
        "--hidden-import=xlrd",
        "--hidden-import=pptx",
        "--hidden-import=py7zr",
        "--hidden-import=tomli",
        "--collect-all=backend", 
        "--collect-all=pillow_heif",
        "--collect-all=xhtml2pdf",
        "--collect-all=reportlab",
        "--collect-all=openpyxl",
        "--collect-all=py7zr",
        "run_app.py"
    ]
    
    print(f"Running build command: {' '.join(args)}")
    subprocess.check_call(args)
    
    print("Build complete. Output in dist/BrutalistConverter")

if __name__ == "__main__":
    # Ensure pyinstaller is installed
    if not shutil.which("pyinstaller"):
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
    build()
