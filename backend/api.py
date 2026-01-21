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

import tempfile


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
