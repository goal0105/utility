import os
import subprocess
from datetime import datetime
import logging
from pathlib import Path
import sys

class Download:
    def __init__(self, output_dir=os.getcwd(), debug=False):
        self.output_dir = output_dir
        self.debug_flag = debug
        self.model_bin = "yt-dlp.exe" 
        self.opts = []

        # Ensure 'uploads' directory exists
        self.uploads_dir = os.path.join(self.output_dir, "uploads")
        os.makedirs(self.uploads_dir, exist_ok=True)

    def download_from_url(self, url):
        try:
            if "youtube" in url.lower():
                
                app_dir = Path(__file__).resolve().parent
                
                logging.info(f"Starting download: {app_dir}")
                download_dir = app_dir / self.uploads_dir

                output_path = "C://Users//Administrator//Downloads//video"
                command = [
                        "yt-dlp",
                        "-P", download_dir,
                        "--cookies-from-browser", "firefox",
                        "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/[height<=720][ext=mp4]",
                        url,
                    ]
                
                logging.info(f"Starting download: {url}")

                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                stdout, stderr = process.communicate()
                process.wait()

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                if process.returncode == 0:
                    logging.info(timestamp +"Download completed successfully.")
                    print(timestamp +": Download completed successfully.")
                    return output_path
                else:
                    logging.error(f"Download failed: {stderr}")
                    print("Error downloading file. Check the log for details.")
                    return None
                
            else :
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"output_file_{timestamp}.mp4"
                output_filepath = os.path.join(self.uploads_dir, output_filename)

                process = subprocess.Popen(
                    [self.model_bin, url, "-o", output_filepath],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                
                stderr = process.communicate()
                process.wait()

                if process.returncode != 0:
                    raise Exception(f"Download failed: {stderr.decode('utf-8')}")

                return output_filepath
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None


# Example Usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download.py <URL>")
        sys.exit(1)

    video_url = sys.argv[1]
    downloader = Download()  # Customize output dir as needed
    # while(1):
    downloader.download_from_url(video_url)