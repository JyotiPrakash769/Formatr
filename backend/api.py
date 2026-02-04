from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import uuid
from backend.core.image_processor import ImageProcessor
from backend.core.pdf_processor import PDFProcessor
from backend.core.av_processor import AVProcessor
from backend.core.doc_processor import DocProcessor
from backend.core.archive_processor import ArchiveProcessor
from backend.core.dev_processor import DevProcessor
from backend.core.smart_detector import SmartDetector
from backend.core.data_processor import DataProcessor
from backend.core.code_formatter import CodeFormatter
from backend.core.office_processor import OfficeProcessor
from backend.core.config_processor import ConfigProcessor

import tempfile
import struct
from pydantic import BaseModel


import subprocess
import platform

router = APIRouter()

@router.post("/open-output-folder")
async def open_output_folder():
    path = OUTPUT_DIR
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
    return {"message": "Folder opened"}

@router.post("/resize/image")
async def resize_image(file: UploadFile = File(...), width: int = Form(None), height: int = Form(None), percentage: int = Form(None)):
    try:
        input_path = save_upload(file)
        # Fix filename
        original_name = file.filename
        temp_renamed = os.path.join(os.path.dirname(input_path), original_name)
        os.replace(input_path, temp_renamed)
        
        output_path = ImageProcessor.resize_image(temp_renamed, width, height, percentage)
        
        # Move to output
        final_path = os.path.join(OUTPUT_DIR, os.path.basename(output_path))
        os.replace(output_path, final_path)
        
        return FileResponse(final_path, filename=os.path.basename(final_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/compress/pdf")
async def compress_pdf(file: UploadFile = File(...), level: str = Form("medium")):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = PDFProcessor.compress_pdf(temp_renamed, level)
        
        final_path = os.path.join(OUTPUT_DIR, os.path.basename(output_path))
        os.replace(output_path, final_path)
        
        return FileResponse(final_path, filename=os.path.basename(final_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Use system temp directory for uploads to avoid permission errors
TEMP_DIR = os.path.join(tempfile.gettempdir(), "formatr_uploads")
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "FORMATR_Output")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_upload(file: UploadFile) -> str:
    path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

@router.post("/convert/image")
async def convert_image(file: UploadFile = File(...), target_format: str = Form(...)):
    try:
        input_path = save_upload(file)
        # Fix filename to original for output
        original_name = file.filename
        temp_renamed = os.path.join(os.path.dirname(input_path), original_name)
        os.replace(input_path, temp_renamed)
        
        output_path = ImageProcessor.convert_image(temp_renamed, target_format, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/compress/image")
async def compress_image(file: UploadFile = File(...), size_kb: int = Form(...)):
    try:
        input_path = save_upload(file)
        original_name = file.filename
        temp_renamed = os.path.join(os.path.dirname(input_path), original_name)
        os.replace(input_path, temp_renamed)
        
        output_path = ImageProcessor.compress_image(temp_renamed, size_kb)
        
        # If output is None (e.g. SVG without compress logic), handle gracefully
        # For now, we assume compress_image handles what it can.
        
        # Move to output dir
        final_path = os.path.join(OUTPUT_DIR, os.path.basename(output_path))
        shutil.move(output_path, final_path)
        
        return FileResponse(final_path, filename=os.path.basename(final_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/pdf-to-image")
async def pdf_to_image(file: UploadFile = File(...), format: str = Form("png")):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_paths = PDFProcessor.convert_pdf_to_images(temp_renamed, format)
        
        # If multiple files, zip them
        if len(output_paths) > 1:
            zip_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file.filename)[0]}_images.zip")
            ArchiveProcessor.create_zip(output_paths, zip_path)
            return FileResponse(zip_path, filename=os.path.basename(zip_path))
        else:
            final_path = os.path.join(OUTPUT_DIR, os.path.basename(output_paths[0]))
            shutil.move(output_paths[0], final_path)
            return FileResponse(final_path, filename=os.path.basename(final_path))
            
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/media")
async def convert_media(file: UploadFile = File(...), target_format: str = Form(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = AVProcessor.convert_media(temp_renamed, target_format, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/doc")
async def convert_doc(file: UploadFile = File(...), target_format: str = Form("pdf")):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = DocProcessor.convert_document(temp_renamed, target_format, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/image-to-pdf")
async def image_to_pdf(file: UploadFile = File(...), percentage: int = Form(100)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        # Resize first if needed using existing method logic (skipping extra API call)
        processed_image = temp_renamed
        if percentage < 100:
             processed_image = ImageProcessor.resize_image(temp_renamed, percentage=percentage)
        
        # Use PDFProcessor to convert single image to PDF
        # We can reuse `convert_images_to_pdf` logic for a list of 1
        output_pdf = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file.filename)[0]}.pdf")
        PDFProcessor.convert_images_to_pdf([processed_image], output_pdf)
        
        return FileResponse(output_pdf, filename=os.path.basename(output_pdf))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/image-to-docx")
async def image_to_docx(file: UploadFile = File(...), percentage: int = Form(100)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        processed_image = temp_renamed
        if percentage < 100:
             processed_image = ImageProcessor.resize_image(temp_renamed, percentage=percentage)
             
        output_docx = DocProcessor.create_docx_from_image(processed_image, OUTPUT_DIR)
        
        return FileResponse(output_docx, filename=os.path.basename(output_docx))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/docx-to-image")
async def docx_to_image(file: UploadFile = File(...), format: str = Form("png")):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        # Step 1: DOCX -> PDF
        # Use a temporary dir for intermediate PDF
        pdf_path = DocProcessor.convert_document(temp_renamed, "pdf", TEMP_DIR)
        
        # Step 2: PDF -> Images
        output_paths = PDFProcessor.convert_pdf_to_images(pdf_path, format)
        
        # Zip or Single
        if len(output_paths) > 1:
            zip_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file.filename)[0]}_images.zip")
            ArchiveProcessor.create_zip(output_paths, zip_path)
            # Move images to output for reference or keep in temp?
            # Existing logic saves images in `TEMP_DIR` effectively because PDF was in TEMP_DIR. 
            # Actually PDFProcessor saves images in `os.path.dirname(file_path)`.
            # So images are in TEMP_DIR.
            return FileResponse(zip_path, filename=os.path.basename(zip_path))
        else:
            final_path = os.path.join(OUTPUT_DIR, os.path.basename(output_paths[0]))
            shutil.move(output_paths[0], final_path)
            return FileResponse(final_path, filename=os.path.basename(final_path))
            
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

class AnalyzeRequest(BaseModel):
    filename: str

@router.post("/analyze")
async def analyze_file(request: AnalyzeRequest):
    return SmartDetector.analyze_file(request.filename)

@router.post("/convert/archive")
async def convert_archive(file: UploadFile = File(...), target_format: str = Form(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = ArchiveProcessor.convert_archive(temp_renamed, target_format, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/extract/images")
async def extract_images(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        ext = os.path.splitext(file.filename)[1].lower()
        output_paths = []
        
        if ext == '.pdf':
            output_paths = PDFProcessor.convert_pdf_to_images(temp_renamed, "png") # Default to PNG
        elif ext == '.docx':
            output_paths = DocProcessor.extract_images_from_docx(temp_renamed, OUTPUT_DIR)
        else:
             return JSONResponse(status_code=400, content={"error": "Unsupported file type for image extraction"})

        if not output_paths:
             return JSONResponse(status_code=404, content={"error": "No images found in document"})

        if len(output_paths) > 1:
            zip_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file.filename)[0]}_extracted_images.zip")
            ArchiveProcessor.create_zip(output_paths, zip_path)
            return FileResponse(zip_path, filename=os.path.basename(zip_path))
        else:
            return FileResponse(output_paths[0], filename=os.path.basename(output_paths[0]))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/extract/audio")
async def extract_audio(file: UploadFile = File(...), format: str = Form("mp3")):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        # FFmpeg handles extraction if we just convert video to audio format
        output_path = AVProcessor.convert_media(temp_renamed, format, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/dev/convert-config")
async def dev_convert_config(file: UploadFile = File(...), target_format: str = Form(...)):
    try:
        input_path = save_upload(file)
        output_path = DevProcessor.convert_config(input_path, target_format, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/dev/base64")
async def dev_base64(file: UploadFile = File(...), action: str = Form(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        if action == 'encode':
            output_path = DevProcessor.base64_encode(temp_renamed, OUTPUT_DIR)
        else:
            output_path = DevProcessor.base64_decode(temp_renamed, OUTPUT_DIR)
            
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/dev/md-to-pdf")
async def dev_md_to_pdf(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = DevProcessor.md_to_pdf(temp_renamed, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

class TranslationRequest(BaseModel):
    source_lang: str
    target_lang: str
    code: str
    api_key: str = None

@router.post("/dev/translate")
async def dev_translate(request: TranslationRequest):
    try:
        # In a real scenario, we would call an LLM API here.
        # For this local demo, we will use basic regex replacement for "Hello World" style code 
        # to demonstrate functionality without needing a real paid key.
        
        # NOTE: A real implementation requires `openai` or `google-generativeai` package.
        
        if request.api_key:
             # Placeholder for Real API call
             # response = client.chat.completions.create(...)
             pass
        
        result = f"# SIMULATED TRANSLATION ({request.source_lang} -> {request.target_lang})\n"
        result += f"# (To enable real translation, integrate an LLM provider)\n\n"
        
        input_code = request.code
        
        # Simple Regex Logic for Demo Purposes
        if request.target_lang == "python":
            result += input_code.replace("System.out.println", "print").replace("console.log", "print").replace(";", "")
        elif request.target_lang == "javascript":
            result += input_code.replace("print", "console.log").replace("System.out.println", "console.log")
        elif request.target_lang == "java":
            result += "public class Main {\n    public static void main(String[] args) {\n        "
            result += input_code.replace("print", "System.out.println").replace("console.log", "System.out.println")
            result += ";\n    }\n}"
        else:
            result += input_code
            
        return {"result": result}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ===== PHASE 1 ENDPOINTS =====

@router.post("/convert/csv-to-json")
async def convert_csv_to_json(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = DataProcessor.csv_to_json(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/json-to-csv")
async def convert_json_to_csv(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = DataProcessor.json_to_csv(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/csv-to-excel")
async def convert_csv_to_excel(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = DataProcessor.csv_to_excel(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/excel-to-csv")
async def convert_excel_to_csv(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = DataProcessor.excel_to_csv(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/video-to-gif")
async def convert_video_to_gif(file: UploadFile = File(...), fps: int = Form(10), width: int = Form(480)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = AVProcessor.video_to_gif(temp_renamed, OUTPUT_DIR, fps, width)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/format/beautify-js")
async def beautify_js(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = CodeFormatter.beautify_js(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/format/minify-js")
async def minify_js(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = CodeFormatter.minify_js(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/format/beautify-css")
async def beautify_css(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = CodeFormatter.beautify_css(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/format/minify-css")
async def minify_css(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = CodeFormatter.minify_css(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/format/beautify-html")
async def beautify_html(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = CodeFormatter.beautify_html(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/format/minify-html")
async def minify_html(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = CodeFormatter.minify_html(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/html-to-pdf")
async def html_to_pdf(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        # Read HTML content
        with open(temp_renamed, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert to PDF using xhtml2pdf
        from xhtml2pdf import pisa
        output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file.filename)[0]}.pdf")
        
        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        
        if pisa_status.err:
            raise Exception("HTML to PDF conversion failed")
        
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ===== PHASE 2 TIER 1 ENDPOINTS =====

@router.post("/convert/excel-to-json")
async def convert_excel_to_json(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = DataProcessor.excel_to_json(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/xls-to-xlsx")
async def convert_xls_to_xlsx(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = DataProcessor.xls_to_xlsx(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/extract/pptx-images")
async def extract_pptx_images(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_folder = OfficeProcessor.extract_pptx_images(temp_renamed, OUTPUT_DIR)
        
        # Create a ZIP of the extracted images
        import shutil
        zip_path = shutil.make_archive(output_folder, 'zip', output_folder)
        return FileResponse(zip_path, filename=os.path.basename(zip_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/extract/pptx-text")
async def extract_pptx_text(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = OfficeProcessor.extract_pptx_text(temp_renamed, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/info/pptx")
async def get_pptx_info(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = OfficeProcessor.get_pptx_info(temp_renamed, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/toml-to-json")
async def convert_toml_to_json(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = ConfigProcessor.toml_to_json(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/toml-to-yaml")
async def convert_toml_to_yaml(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = ConfigProcessor.toml_to_yaml(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/env-to-json")
async def convert_env_to_json(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = ConfigProcessor.env_to_json(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/json-to-env")
async def convert_json_to_env(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = ConfigProcessor.json_to_env(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/validate/env")
async def validate_env(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        output_path = ConfigProcessor.validate_env(input_path, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/convert/7z-to-zip")
async def convert_7z_to_zip(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_path = ArchiveProcessor.convert_7z_to_zip(temp_renamed, OUTPUT_DIR)
        return FileResponse(output_path, filename=os.path.basename(output_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/extract/7z")
async def extract_7z(file: UploadFile = File(...)):
    try:
        input_path = save_upload(file)
        temp_renamed = os.path.join(os.path.dirname(input_path), file.filename)
        os.replace(input_path, temp_renamed)
        
        output_folder = ArchiveProcessor.extract_7z(temp_renamed, OUTPUT_DIR)
        
        # Create a ZIP of the extracted contents
        import shutil
        zip_path = shutil.make_archive(output_folder, 'zip', output_folder)
        return FileResponse(zip_path, filename=os.path.basename(zip_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

