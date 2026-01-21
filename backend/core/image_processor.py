import os
import io
from PIL import Image

class ImageProcessor:
    SUPPORTED_FORMATS = ['PNG', 'JPEG', 'JPG', 'WEBP']

    @staticmethod
    def convert_image(file_path: str, target_format: str, output_dir: str = None) -> str:
        """
        Convert an image to a specific format.
        """
        if target_format.upper() not in ImageProcessor.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {target_format}")

        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        
        if output_dir is None:
            output_dir = os.path.dirname(file_path)
            
        output_path = os.path.join(output_dir, f"{name}.{target_format.lower()}")
        
        # Handle SVG separately
        if ext.lower() == '.svg':
            drawing = svg2rlg(file_path)
            if target_format.lower() == 'png':
                renderPM.drawToFile(drawing, output_path, fmt="PNG")
            elif target_format.lower() == 'jpg' or target_format.lower() == 'jpeg':
                renderPM.drawToFile(drawing, output_path, fmt="JPG")
            else:
                 # Fallback for others, render to PNG then convert
                 temp_png = output_path + ".png"
                 renderPM.drawToFile(drawing, temp_png, fmt="PNG")
                 with Image.open(temp_png) as img:
                     img.save(output_path)
                 os.remove(temp_png)
            return output_path

        # Standard Image handling (includes HEIC, TIFF)
        with Image.open(file_path) as img:
            if target_format.upper() in ["JPG", "JPEG"]:
                # Handle alpha channel for JPEG
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                else:
                    img = img.convert("RGB")
            img.save(output_path)
            
        return output_path

    @staticmethod
    def resize_image(file_path: str, width: int = None, height: int = None, percentage: int = None) -> str:
        """
        Resize image by fixed width/height or percentage.
        """
        img = Image.open(file_path)
        original_width, original_height = img.size
        
        new_width, new_height = original_width, original_height

        if percentage:
            scale = percentage / 100
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
        elif width and height:
            new_width = width
            new_height = height
        elif width:
            ratio = width / original_width
            new_width = width
            new_height = int(original_height * ratio)
        elif height:
            ratio = height / original_height
            new_height = height
            new_width = int(original_width * ratio)
            
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        output_path = file_path # Overwrite or new? Let's assume overwrite for "processing" unless specified otherwise.
        # Ideally, we should create a new file or add a suffix. Let's add suffix.
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_resized{ext}"
        
        resized_img.save(output_path)
        return output_path

    @staticmethod
    def compress_image(file_path: str, target_size_kb: int) -> str:
        """
        Compress image to target size in KB.
        """
        # SVG/HEIC compression is complex, for now convert to JPG then compress
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        
        if ext.lower() in ['.svg', '.heic', '.heif']:
             # Pre-convert to JPG for compression
             temp_jpg = os.path.join(os.path.dirname(file_path), f"{name}_temp.jpg")
             ImageProcessor.convert_image(file_path, "JPG", os.path.dirname(file_path))
             file_path = temp_jpg # Proceed with this new file
        
        img = Image.open(file_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        output_path = os.path.join(os.path.dirname(file_path), f"compressed_{name}.jpg")
        
        # Binary search for quality
        min_quality = 10
        max_quality = 95
        
        while min_quality <= max_quality:
            quality = (min_quality + max_quality) // 2
            img.save(output_path, "JPEG", optimize=True, quality=quality)
            
            size_kb = os.path.getsize(output_path) / 1024
            
            if size_kb <= target_size_kb:
                min_quality = quality + 1
            else:
                max_quality = quality - 1
                
        return output_path
