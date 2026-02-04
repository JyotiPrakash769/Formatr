import os
import zipfile
import shutil
import tarfile
import py7zr

class ArchiveProcessor:
    @staticmethod
    def convert_archive(input_path: str, target_format: str, output_dir: str) -> str:
        """
        Convert archive formats: zip -> tar.gz, tar -> zip, etc.
        target_format: 'zip', 'tar', 'gztar', 'bztar', 'xztar'
        """
        # Create temp dir for extraction
        temp_extract_dir = os.path.join(os.path.dirname(input_path), "temp_extract")
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        os.makedirs(temp_extract_dir)
        
        try:
            # Extract based on extension
            shutil.unpack_archive(input_path, temp_extract_dir)
            
            # Repack
            base_name = os.path.join(output_dir, os.path.splitext(os.path.basename(input_path))[0])
            output_file = shutil.make_archive(base_name, target_format, temp_extract_dir)
            
            return output_file
        finally:
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)
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
    
    @staticmethod
    def extract_7z(archive_path: str, output_dir: str = None) -> str:
        """Extract 7Z archive"""
        if output_dir is None:
            base, _ = os.path.splitext(archive_path)
            output_dir = base
        
        os.makedirs(output_dir, exist_ok=True)
        
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            archive.extractall(path=output_dir)
        
        return output_dir
    
    @staticmethod
    def create_7z(source_path: str, output_path: str) -> str:
        """Create 7Z archive from file or directory"""
        with py7zr.SevenZipFile(output_path, 'w') as archive:
            if os.path.isdir(source_path):
                archive.writeall(source_path, arcname=os.path.basename(source_path))
            else:
                archive.write(source_path, arcname=os.path.basename(source_path))
        
        return output_path
    
    @staticmethod
    def convert_7z_to_zip(input_path: str, output_dir: str) -> str:
        """Convert 7Z to ZIP"""
        # Extract to temp
        temp_extract_dir = os.path.join(os.path.dirname(input_path), "temp_7z_extract")
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        os.makedirs(temp_extract_dir)
        
        try:
            # Extract 7Z
            with py7zr.SevenZipFile(input_path, mode='r') as archive:
                archive.extractall(path=temp_extract_dir)
            
            # Create ZIP
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.zip")
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_extract_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_extract_dir)
                        zipf.write(file_path, arcname)
            
            return output_path
        finally:
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)
