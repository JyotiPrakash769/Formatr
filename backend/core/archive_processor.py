import os
import zipfile
import shutil

class ArchiveProcessor:
    @staticmethod
    def create_zip(source_paths: list[str], output_path: str):
        """
        Compress multiple files into a ZIP archive.
        """
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_paths:
                if os.path.isdir(file_path):
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            abs_file = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_file, os.path.dirname(source_paths[0])) # approximates relative path
                            zipf.write(abs_file, rel_path)
                else:
                    zipf.write(file_path, os.path.basename(file_path))
        return output_path

    @staticmethod
    def extract_zip(zip_path: str, output_dir: str = None) -> str:
        """
        Extract ZIP archive.
        """
        if output_dir is None:
            base, _ = os.path.splitext(zip_path)
            output_dir = base # Extract to folder with same name
            
        os.makedirs(output_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(output_dir)
            
        return output_dir
