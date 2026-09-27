import subprocess
from pathlib import Path


# ============================================================
# CREATE FINAL SHORT
# ============================================================

def create_final_short(
    video_path: str,
    subtitle_path: str,
    short_id: int
):

    output_folder = Path("final_shorts")
    output_folder.mkdir(exist_ok=True)

    output_path = output_folder / f"final_short_{short_id}.mp4"

    # --------------------------------------------------------
    # Prepare subtitle path for FFmpeg
    # --------------------------------------------------------

    subtitle_file = Path(
        subtitle_path
    ).resolve()

    subtitle_filter_path = str(
        subtitle_file
    ).replace("\\", "/")

    subtitle_filter_path = (
        subtitle_filter_path
        .replace(":", "\\:")
        .replace("'", "\\'")
    )

    # --------------------------------------------------------
    # 9:16 + styled captions
    # --------------------------------------------------------

    video_filter = (
        "scale=1080:1920:"
        "force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"subtitles='{subtitle_filter_path}':"
        "force_style="
        "'FontName=Arial,"
        "FontSize=32,"
        "Bold=1,"
        "PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "Outline=3,"
        "Shadow=1,"
        "Alignment=2,"
        "MarginV=160'"
    )

    # --------------------------------------------------------
    # FFmpeg command
    # --------------------------------------------------------

    command = [
        "ffmpeg",

        "-i",
        video_path,

        # ----------------------------------------------------
        # Video processing
        # ----------------------------------------------------

        "-vf",
        video_filter,

        # ----------------------------------------------------
        # Explicit video + audio
        # ----------------------------------------------------

        "-map",
        "0:v:0",

        "-map",
        "0:a:0?",

        # ----------------------------------------------------
        # Video encoding
        # ----------------------------------------------------

        "-c:v",
        "libx264",

        "-preset",
        "medium",

        "-crf",
        "23",

        # ----------------------------------------------------
        # Audio encoding
        # ----------------------------------------------------

        "-c:a",
        "aac",

        "-b:a",
        "192k",

        # ----------------------------------------------------
        # Keep duration aligned
        # ----------------------------------------------------

        "-shortest",

        # ----------------------------------------------------
        # Overwrite existing file
        # ----------------------------------------------------

        "-y",

        str(output_path)
    ]

    print("\n🔥 Creating FINAL SHORT...")
    print(f"📥 Video:     {video_path}")
    print(f"📝 Subtitles: {subtitle_path}")

    subprocess.run(
        command,
        check=True
    )

    print(
        f"\n✅ FINAL SHORT CREATED:"
        f" {output_path}"
    )

    return str(output_path)