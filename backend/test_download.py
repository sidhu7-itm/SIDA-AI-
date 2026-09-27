from app.services.video_downloader import download_video

url = "https://youtu.be/1wjFQsrXhK0?si=5DGkx252vk3uBNK0"

print("Starting download...")

path = download_video(url, 1)

print("Download completed!")
print("Saved at:", path)