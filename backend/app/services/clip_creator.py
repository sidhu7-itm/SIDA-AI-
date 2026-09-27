import subprocess
from pathlib import Path


# ============================================================
# CREATE CLIP
# ============================================================

def create_clip(
    video_path: str,
    start_time: float,
    end_time: float,
    clip_id: int
):

    output_folder = Path("clips")
    output_folder.mkdir(exist_ok=True)

    output_path = output_folder / f"clip_{clip_id}.mp4"

    duration = end_time - start_time

    command = [
        "ffmpeg",

        # ----------------------------------------------------
        # Start time
        # ----------------------------------------------------

        "-ss",
        str(start_time),

        # ----------------------------------------------------
        # Input video
        # ----------------------------------------------------

        "-i",
        video_path,

        # ----------------------------------------------------
        # Clip duration
        # ----------------------------------------------------

        "-t",
        str(duration),

        # ----------------------------------------------------
        # Explicitly select video + audio
        # ----------------------------------------------------

        "-map",
        "0:v:0",

        "-map",
        "0:a:0?",

        # ----------------------------------------------------
        # Video
        # ----------------------------------------------------

        "-c:v",
        "libx264",

        # ----------------------------------------------------
        # Audio
        # ----------------------------------------------------

        "-c:a",
        "aac",

        "-b:a",
        "192k",

        # ----------------------------------------------------
        # Replace existing file
        # ----------------------------------------------------

        "-y",

        str(output_path)
    ]

    print("\n🎬 Creating clip...")
    print(f"📥 Input: {video_path}")
    print(f"⏱️ Time: {start_time:.2f}s → {end_time:.2f}s")

    subprocess.run(
        command,
        check=True
    )

    print(f"✅ Created: {output_path}")

    return str(output_path)