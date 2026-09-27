import yt_dlp
from pathlib import Path


def download_video(youtube_url: str, video_id: int):

    output_folder = Path("downloads")
    output_folder.mkdir(exist_ok=True)

    options = {
        "outtmpl": str(output_folder / f"video_{video_id}.%(ext)s"),

        "format": "bestvideo+bestaudio/best",

        "merge_output_format": "mp4",

        "noplaylist": True,

        "ffmpeg_location": r"C:\Users\banal\Downloads\ffmpeg-9.0.1-essentials_build\ffmpeg-9.0.1-essentials_build\bin"
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([youtube_url])

    return str(output_folder / f"video_{video_id}.mp4")