import yt_dlp

# Define resolution format mapping
resolution_formats = {
    '4k': 'bestvideo[height=2160]+bestaudio/best',
    '1080p': 'bestvideo[height=1080]+bestaudio/best',
    '720p': 'bestvideo[height=720]+bestaudio/best'
}

try:
    video_url = input("Enter YouTube video URL: ").strip()
    print("Choose resolution:")
    print("1. 4K")
    print("2. 1080p")
    print("3. 720p")
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == '1':
        selected_format = resolution_formats['4k']
    elif choice == '2':
        selected_format = resolution_formats['1080p']
    elif choice == '3':
        selected_format = resolution_formats['720p']
    else:
        print("Invalid choice. Defaulting to best available.")
        selected_format = 'best'

    ydl_opts = {
        'format': selected_format,
        'merge_output_format': 'mp4',
        'outtmpl': '/Users/prabinkumargupta/Downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading in selected resolution ({choice})...")
        ydl.download([video_url])
        print("Download completed!")

except Exception as e:
    print("An error occurred:", e)
