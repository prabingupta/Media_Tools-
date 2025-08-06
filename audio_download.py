import os
from yt_dlp import YoutubeDL

def clean_url(url: str) -> str:
    if "youtube.com/shorts/" in url:
        video_id = url.split("/shorts/")[1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url.strip()

def download_audio(url: str, output_folder: str = "downloads") -> str:
    try:
        url = clean_url(url)
        os.makedirs(output_folder, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'no_warnings': True,
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                              'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                              'Chrome/115.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            mp3_filename = os.path.join(output_folder, f"{title}.mp3")

            if os.path.exists(mp3_filename):
                return f"Downloaded and converted to MP3: {mp3_filename}"
            else:
                return "Failed to find the converted MP3 file after download."

    except Exception as e:
        return f"Failed to download:\n{str(e)}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python audio_download.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    print(download_audio(url))
