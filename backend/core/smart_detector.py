import os
import mimetypes

class SmartDetector:
    @staticmethod
    def analyze_file(filename: str) -> dict:
        """
        Analyze file extension and return recommended actions.
        """
        base, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        actions = []
        category = "unknown"

        # Image
        if ext in ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.heic', '.svg', '.gif']:
            category = "image"
            actions = [
                {"id": "convert_image", "name": "Convert Format (PNG/JPG/WEBP/PDF)", "type": "convert"},
                {"id": "resize_image", "name": "Resize / Scale", "type": "resize"},
                {"id": "compress_image", "name": "Compress", "type": "compress"},
                {"id": "image_to_pdf", "name": "Convert to PDF", "type": "convert"},
                {"id": "image_to_docx", "name": "Convert to DOCX", "type": "convert"}
            ]

        # PDF
        elif ext == '.pdf':
            category = "document"
            actions = [
                {"id": "compress_pdf", "name": "Compress PDF", "type": "compress"},
                {"id": "pdf_to_image", "name": "Convert to Images", "type": "convert"},
                {"id": "extract_media_pdf", "name": "Extract Images from PDF", "type": "extract"}
            ]

        # Document (DOCX)
        elif ext == '.docx':
            category = "document"
            actions = [
                {"id": "doc_to_pdf", "name": "Convert to PDF", "type": "convert"},
                {"id": "extract_media_doc", "name": "Extract Images from DOCX", "type": "extract"}
            ]

        # Markdown
        elif ext == '.md':
            category = "developer"
            actions = [
                {"id": "md_to_pdf", "name": "Convert to PDF", "type": "convert"}
            ]

        # Video
        elif ext in ['.mp4', '.mkv', '.mov', '.avi', '.webm', '.flv']:
            category = "video"
            actions = [
                {"id": "convert_video", "name": "Convert Video", "type": "convert"},
                {"id": "extract_audio", "name": "Extract Audio (MP3)", "type": "extract"},
                {"id": "video_to_gif", "name": "Convert to GIF", "type": "convert"}
            ]

        # Audio
        elif ext in ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a']:
            category = "audio"
            actions = [
                {"id": "convert_audio", "name": "Convert Audio", "type": "convert"}
            ]

        # Archive
        elif ext in ['.zip', '.tar', '.gz', '.tgz', '.7z']:
            category = "archive"
            actions = [
                {"id": "convert_archive", "name": "Convert Archive Format", "type": "convert"},
            ]
            if ext == '.7z':
                actions.append({"id": "7z_to_zip", "name": "Convert 7Z to ZIP", "type": "convert"})

        # Data Files (CSV/Excel)
        elif ext == '.csv':
            category = "data"
            actions = [
                {"id": "csv_to_json", "name": "Convert to JSON", "type": "convert"},
                {"id": "csv_to_excel", "name": "Convert to Excel (XLSX)", "type": "convert"}
            ]
        
        # Excel Files
        elif ext in ['.xlsx', '.xls']:
            category = "data"
            actions = [
                {"id": "excel_to_csv", "name": "Convert to CSV", "type": "convert"},
                {"id": "excel_to_json", "name": "Convert to JSON", "type": "convert"}
            ]
            if ext == '.xls':
                actions.append({"id": "xls_to_xlsx", "name": "Upgrade to XLSX", "type": "convert"})
        
        # PowerPoint Files
        elif ext == '.pptx':
            category = "office"
            actions = [
                {"id": "extract_pptx_images", "name": "Extract Images", "type": "extract"},
                {"id": "extract_pptx_text", "name": "Extract Text", "type": "extract"},
                {"id": "pptx_info", "name": "Get Info", "type": "info"}
            ]
        
        # TOML Config
        elif ext == '.toml':
            category = "config"
            actions = [
                {"id": "toml_to_json", "name": "Convert to JSON", "type": "convert"},
                {"id": "toml_to_yaml", "name": "Convert to YAML", "type": "convert"}
            ]
        
        # ENV Files
        elif ext == '.env':
            category = "config"
            actions = [
                {"id": "env_to_json", "name": "Convert to JSON", "type": "convert"},
                {"id": "validate_env", "name": "Validate ENV File", "type": "validate"}
            ]

        # Config Files (JSON/YAML/XML)
        elif ext in ['.json', '.yaml', '.yml', '.xml']:
            category = "developer"
            actions = [
                {"id": "convert_config", "name": "Convert Config Format", "type": "convert"}
            ]
            if ext == '.json':
                actions.append({"id": "json_to_csv", "name": "Convert to CSV", "type": "convert"})

        # HTML
        elif ext in ['.html', '.htm']:
            category = "web"
            actions = [
                {"id": "html_to_pdf", "name": "Convert to PDF", "type": "convert"},
                {"id": "beautify_html", "name": "Beautify/Format HTML", "type": "format"},
                {"id": "minify_html", "name": "Minify HTML", "type": "format"}
            ]

        # JavaScript
        elif ext == '.js':
            category = "code"
            actions = [
                {"id": "beautify_js", "name": "Beautify/Format JS", "type": "format"},
                {"id": "minify_js", "name": "Minify JS", "type": "format"}
            ]

        # CSS
        elif ext == '.css':
            category = "code"
            actions = [
                {"id": "beautify_css", "name": "Beautify/Format CSS", "type": "format"},
                {"id": "minify_css", "name": "Minify CSS", "type": "format"}
            ]

        # All Files
        if ext.endswith('.b64.txt') or (ext == '.txt' and 'b64' in base):
             actions.append({"id": "base64_decode", "name": "Base64 Decode", "type": "utility"})
        else:
             actions.append({"id": "base64_encode", "name": "Base64 Encode", "type": "utility"})

        return {
            "filename": filename,
            "extension": ext,
            "category": category,
            "actions": actions
        }
