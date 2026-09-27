from app.services.transcription import transcribe_video


video_path = "downloads/vidssave.com ONE Habit That Changes Everything — Dr. Vikas Divyakirti _ Raj Shamani Clips 240P.mp4"

print("Starting transcription...")

result = transcribe_video(video_path)

for segment in result:
    print(
        f"[{segment['start']:.2f}s - {segment['end']:.2f}s] "
        f"{segment['text']}"
    )

print("Transcription completed!")