from app.services.transcription import transcribe_video
from app.services.ai_selector import select_moments
import json

video_path = "downloads/video_1.mp4"

print("🎬 Transcribing REAL video...")
transcript = transcribe_video(video_path)

print("\n📝 TRANSCRIPT CREATED")
print(json.dumps(transcript, indent=2))

print("\n🤖 AI IS SELECTING MOMENTS...")
results = select_moments(transcript)

print("\n🔥 AI SELECTED MOMENTS:")
print(json.dumps(results, indent=2))