import subprocess
from pathlib import Path


# ============================================================
# CREATE VERTICAL SHORT
# ============================================================

def create_vertical_short(
    video_path: str,
    short_id: int
):

    output_folder = Path("shorts")
    output_folder.mkdir(exist_ok=True)

    output_path = output_folder / f"short_{short_id}.mp4"

    command = [
        "ffmpeg",

        "-i",
        video_path,

        # ----------------------------------------------------
        # Convert video to 9:16
        # ----------------------------------------------------

        "-vf",
        (
            "scale=1080:1920:"
            "force_original_aspect_ratio=increase,"
            "crop=1080:1920"
        ),

        # ----------------------------------------------------
        # Video / audio encoding
        # ----------------------------------------------------

        "-c:v",
        "libx264",

        "-preset",
        "medium",

        "-crf",
        "23",

        "-c:a",
        "aac",

        "-y",

        str(output_path)
    ]

    subprocess.run(
        command,
        check=True
    )

    return str(output_path)