from app.services.transcription import transcribe_video
from app.services.ai_selector import select_moments
from app.services.clip_creator import create_clip
import json


# --------------------------------------------------
# VIDEO TO TEST
# --------------------------------------------------

video_path = "downloads/video_1.mp4"


# --------------------------------------------------
# STEP 1: TRANSCRIBE VIDEO
# --------------------------------------------------

print("🎙️ Transcribing video...")

transcript = transcribe_video(video_path)

print(f"✅ Transcript created: {len(transcript)} segments")


# --------------------------------------------------
# STEP 2: SEND REAL TRANSCRIPT TO AI
# --------------------------------------------------

moments = select_moments(transcript)


# --------------------------------------------------
# STEP 3: SHOW AI RESULTS
# --------------------------------------------------

print("\n🔥 AI SELECTED MOMENTS:\n")

print(json.dumps(moments, indent=2))


# --------------------------------------------------
# STEP 4: STOP IF NO VALID MOMENTS
# --------------------------------------------------

if not moments:
    print("\n❌ No valid moments were selected.")
    print("🛑 Clip creation stopped.")
    raise SystemExit


# --------------------------------------------------
# STEP 5: CREATE ACTUAL CLIPS
# --------------------------------------------------

print("\n🎬 CREATING CLIPS...\n")


created_clips = []

for clip_id, moment in enumerate(moments, start=1):

    start_time = moment["start"]
    end_time = moment["end"]

    reason = moment.get("reason", "")

    print(
        f"🎞️ Clip {clip_id}: "
        f"{start_time:.2f}s → {end_time:.2f}s"
    )

    if reason:
        print(f"💡 Reason: {reason}")

    try:

        output_path = create_clip(
            video_path=video_path,
            start_time=start_time,
            end_time=end_time,
            clip_id=clip_id
        )

        created_clips.append(output_path)

        print(f"✅ Created: {output_path}\n")

    except Exception as error:

        print(
            f"❌ Failed to create clip {clip_id}: "
            f"{error}\n"
        )


# --------------------------------------------------
# STEP 6: FINAL RESULT
# --------------------------------------------------

print("===================================")
print("🎉 SIDA-AI TEST COMPLETE")
print("===================================")

if created_clips:

    print(f"\n✅ Successfully created {len(created_clips)} clip(s):\n")

    for clip in created_clips:
        print(f"🎬 {clip}")

else:

    print("\n❌ No clips were created.")