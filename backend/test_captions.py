from app.services.transcription import transcribe_video
from app.services.caption_creator import create_srt


# ============================================================
# TEST VIDEO
# ============================================================

video_path = "downloads/video_1.mp4"


# ============================================================
# TRANSCRIBE
# ============================================================

print("🎙️ Transcribing video...")

transcript = transcribe_video(video_path)

print(f"✅ Transcript created: {len(transcript)} segments")


# ============================================================
# TEST CLIP RANGE
# ============================================================

clip_start = 0.0
clip_end = 45.0


# ============================================================
# CREATE SUBTITLE FILE
# ============================================================

print("\n📝 Creating subtitles...")

subtitle_path = create_srt(
    transcript=transcript,
    clip_start=clip_start,
    clip_end=clip_end,
    subtitle_id=1
)


# ============================================================
# RESULT
# ============================================================

print("\n===================================")
print("🎉 CAPTION TEST COMPLETE")
print("===================================")

print(f"\n📝 Subtitle file:")
print(subtitle_path)