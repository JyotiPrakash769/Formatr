import os
import subprocess
import shutil
import sys
from docx2pdf import convert

class DocProcessor:
    @staticmethod
    def get_soffice_path():
        # Common paths for Windows
        paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        ]
        
        # Check if in PATH
        if shutil.which("soffice"):
            return "soffice"
            
        for p in paths:
            if os.path.exists(p):
                return p
                
        # If not found, maybe just try 'soffice' and hope or raise error
    def convert_document(file_path: str, target_format: str, output_dir: str) -> str:
        """
        Convert document to target format.
        Supported: DOCX -> PDF
        """
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.{target_format}")
        
        if ext.lower() == '.docx' and target_format.lower() == 'pdf':
            # Use docx2pdf (requires Word installed on Windows/Mac)
            if platform.system() == "Windows":
                 convert(file_path, output_path)
            else:
                 # FLallback or LibreOffice
                 subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, file_path], check=True)
            return output_path
            
        raise ValueError(f"Unsupported conversion: {ext} to {target_format}")

    @staticmethod
    def create_docx_from_image(image_path: str, output_dir: str) -> str:
        """
        Create a DOCX file containing the image.
        """
        filename = os.path.basename(image_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.docx")
        
        doc = Document()
        # Add image, fitting to page width roughly (6 inches is safe margin)
        doc.add_picture(image_path, width=Inches(6))
        doc.save(output_path)
        
        return output_path
