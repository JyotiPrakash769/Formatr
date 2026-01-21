from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app = FastAPI(title="FORMATR", version="1.0.0")

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

import sys

# Serve Frontend Static Files
# Handle PyInstaller _MEIPASS
if getattr(sys, 'frozen', False):
    bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    frontend_path = os.path.join(bundle_dir, "frontend")
else:
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

from backend.api import router as api_router
app.include_router(api_router, prefix="/api")

@app.get("/api/status")
async def status():
    return {"status": "running", "message": "Brutalist Engine Online"}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(frontend_path, "logo.png"))

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
