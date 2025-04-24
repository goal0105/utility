
import sys
from downloader import Download
   
# Example Usage  youtube downloader
if __name__ == "__main__":

    downloader = Download()   
    with open("youtube_url.txt", "r", encoding="utf-8") as f:
        for url in f:
            print(url)
            downloader.download_from_url(url)
