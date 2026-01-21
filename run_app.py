import sys
import os
import threading
import time
import socket
import uvicorn
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
import traceback

# Setup logging to file for debugging frozen app
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug.log")
def log_error(msg):
    with open(log_file, "a") as f:
        f.write(msg + "\n")

try:
    from backend.main import app
except Exception as e:
    log_error(f"Import Error: {traceback.format_exc()}")
    # We still need basic app to show error if possible, but it will likely fail.
    raise e

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

PORT = get_free_port()

def start_server():
    # Fix for backend logging in frozen app (no console)
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")

    try:
        # use_colors=False to prevent isatty check failure
        uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info", use_colors=False)
    except Exception as e:
        log_error(f"Server Error: {traceback.format_exc()}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FORMATR")
        self.setGeometry(100, 100, 1000, 800)
        
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl(f"http://127.0.0.1:{PORT}"))

if __name__ == "__main__":
    try:
        # Start API in a separate thread
        api_thread = threading.Thread(target=start_server, daemon=True)
        api_thread.start()

        # Give the server a moment to spin up
        time.sleep(2)

        # Fix Taskbar Icon (Windows)
        try:
            import ctypes
            myappid = 'antigravity.brutal_converter.1.0.0' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        qt_app = QApplication(sys.argv)
        
        # Set Window Icon
        if getattr(sys, 'frozen', False):
             bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
             icon_path = os.path.join(bundle_dir, "frontend", "logo.png")
        else:
             icon_path = os.path.join(os.path.dirname(__file__), "frontend", "logo.png")
             
        if os.path.exists(icon_path):
            qt_app.setWindowIcon(QIcon(icon_path))
            
        window = MainWindow()
        if os.path.exists(icon_path):
            window.setWindowIcon(QIcon(icon_path))
            
        window.show()
        sys.exit(qt_app.exec())
    except Exception as e:
        log_error(f"Main Error: {traceback.format_exc()}")
        sys.exit(1)
