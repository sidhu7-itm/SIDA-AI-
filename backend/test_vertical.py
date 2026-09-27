from app.services.vertical_formatter import create_vertical_short


video_path = "clips/clip_1.mp4"


print("📱 Converting clip to 9:16...")


output = create_vertical_short(
    video_path=video_path,
    short_id=1
)


print("\n✅ Vertical Short created:")
print(output)