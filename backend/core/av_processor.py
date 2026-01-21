import os
import subprocess
import shutil

class AVProcessor:
    @staticmethod
    def check_ffmpeg():
        if not shutil.which("ffmpeg"):
            raise EnvironmentError("FFmpeg not found in system PATH.")

    @staticmethod
    def convert_media(file_path: str, target_format: str, output_dir: str = None) -> str:
        """
        Convert audio or video to target format using FFmpeg.
        """
        try:
            filename = os.path.basename(file_path)
            name_no_ext = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{name_no_ext}.{target_format}")
            
            # Ensure ffmpeg is available
            AVProcessor.check_ffmpeg()
            
            cmd = [
                "ffmpeg",
                "-i", file_path,
                output_path
            ]
            
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}")
            
    @staticmethod
    def compress_video(file_path: str, target_res: str = None, bitrate: str = None) -> str:
        """
        Compress video by changing resolution or bitrate.
        target_res: e.g. "1280x720" or "scale=-1:720"
        bitrate: e.g. "1M", "500k"
        """
        AVProcessor.check_ffmpeg()
        
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_compressed{ext}"
        
        cmd = ["ffmpeg", "-i", file_path, "-y"]
        
        if target_res:
            # simple scaling
            cmd.extend(["-vf", f"scale={target_res}"])
            
        if bitrate:
            cmd.extend(["-b:v", bitrate])
            
        cmd.append(output_path)
        
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg compression failed: {process.stderr.decode()}")
            
        return output_path
