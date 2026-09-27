from app.services.subtitle_burner import burn_subtitles


# ============================================================
# TEST FILES
# ============================================================

video_path = "clips/clip_1.mp4"

subtitle_path = "subtitles/subtitle_1.srt"


# ============================================================
# BURN SUBTITLES
# ============================================================

print("📝 Starting subtitle test...")


output = burn_subtitles(
    video_path=video_path,
    subtitle_path=subtitle_path,
    output_id=1
)


# ============================================================
# RESULT
# ============================================================

print("\n===================================")
print("🎉 SUBTITLE BURN TEST COMPLETE")
print("===================================")

print(f"\n🔥 Final video:")
print(output)