import os
import fitz # PyMuPDF

class PDFProcessor:
    @staticmethod
    def convert_pdf_to_images(file_path: str, output_format: str = 'png') -> list[str]:
        """
        Convert PDF pages to images.
        """
        doc = fitz.open(file_path)
        output_paths = []
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = os.path.dirname(file_path)

        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap()
            output_name = f"{base_name}_page_{i+1}.{output_format}"
            output_path = os.path.join(output_dir, output_name)
            pix.save(output_path)
            output_paths.append(output_path)
        
        return output_paths

    @staticmethod
    def compress_pdf(file_path: str, level: str = 'medium') -> str:
        """
        Compress PDF.
        Level: low (less compression), medium, high (max compression)
        Uses garbage collection and deflate.
        """
        doc = fitz.open(file_path)
        
        # Map levels to garbage collection options
        # 0: no garbage collection
        # 1: unreferenced objects
        # 2: unreferenced objects + streams
        # 3: unreferenced objects + streams + fonts
        # 4: check streams for duplication
        
        gc_level = 4
        deflate = True
        
        if level == 'low':
            gc_level = 1
        elif level == 'high':
            pass
            
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_compressed{ext}"
        
        doc.save(output_path, garbage=gc_level, deflate=deflate, clean=True)
        return output_path

    @staticmethod
    def convert_images_to_pdf(image_paths: list[str], output_path: str):
        """
        Convert list of images to a single PDF.
        """
        doc = fitz.open()
        for img_path in image_paths:
            img = fitz.open(img_path)
            rect = img[0].rect
            pdfbytes = img.convert_to_pdf()
            img.close()
            imgPDF = fitz.open("pdf", pdfbytes)
            page = doc.new_page(width=rect.width, height=rect.height)
            page.show_pdf_page(rect, imgPDF, 0)
        
        doc.save(output_path)
        return output_path
