
import sys
from downloader import Download
   
# Example Usage  youtube downloader
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download.py <URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    downloader = Download()   
    downloader.download_from_url(youtube_url)