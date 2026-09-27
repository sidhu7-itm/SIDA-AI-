from app.services.final_renderer import create_final_short


# ============================================================
# TEST FILES
# ============================================================

video_path = "clips/clip_1.mp4"

subtitle_path = "subtitles/subtitle_1.srt"


# ============================================================
# CREATE FINAL SHORT
# ============================================================

print("🚀 Starting final Short rendering...")


output = create_final_short(
    video_path=video_path,
    subtitle_path=subtitle_path,
    short_id=1
)


# ============================================================
# RESULT
# ============================================================

print("\n===================================")
print("🎉 FINAL SHORT TEST COMPLETE")
print("===================================")

print(f"\n🔥 Final clip:")
print(output)