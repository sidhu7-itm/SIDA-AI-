from app.services.clip_creator import create_clip


video_path = "downloads/video_5.mp4"

print("Creating clip...")

clip_path = create_clip(
    video_path,
    46.24,
    60.08,
    1
)

print("Clip created!")
print("Saved at:", clip_path)