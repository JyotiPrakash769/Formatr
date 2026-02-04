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
    
    @staticmethod
    def video_to_gif(file_path: str, output_dir: str, fps: int = 10, width: int = 480) -> str:
        """
        Convert video to optimized GIF with palette generation.
        fps: frames per second (lower = smaller file)
        width: output width in pixels (height auto-scaled)
        """
        AVProcessor.check_ffmpeg()
        
        filename = os.path.basename(file_path)
        name_no_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{name_no_ext}.gif")
        palette_path = os.path.join(output_dir, f"{name_no_ext}_palette.png")
        
        try:
            # Step 1: Generate palette for better quality
            palette_cmd = [
                "ffmpeg", "-i", file_path,
                "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,palettegen",
                "-y", palette_path
            ]
            subprocess.run(palette_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Step 2: Create GIF using palette
            gif_cmd = [
                "ffmpeg", "-i", file_path, "-i", palette_path,
                "-lavfi", f"fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
                "-y", output_path
            ]
            subprocess.run(gif_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Cleanup palette
            if os.path.exists(palette_path):
                os.remove(palette_path)
            
            return output_path
        except subprocess.CalledProcessError as e:
            if os.path.exists(palette_path):
                os.remove(palette_path)
            raise RuntimeError(f"Video to GIF conversion failed: {e.stderr.decode()}")

