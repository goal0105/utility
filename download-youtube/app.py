
import sys
from downloader import Download
   
# Example Usage  
if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python download.py <URL>")
    #     sys.exit(1)

    # video_url = sys.argv[1]
    downloader = Download()  # Customize output dir as needed
    downloader.download_from_url("https://www.youtube.com/watch?v=1MwSoB0gnM4")
 

    