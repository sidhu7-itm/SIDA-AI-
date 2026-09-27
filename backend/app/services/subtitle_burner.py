import subprocess
from pathlib import Path


# ============================================================
# BURN STYLED SUBTITLES INTO VIDEO
# ============================================================

def burn_subtitles(
    video_path: str,
    subtitle_path: str,
    output_id: int
):

    output_folder = Path("captioned")
    output_folder.mkdir(exist_ok=True)

    output_path = output_folder / f"captioned_{output_id}.mp4"

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
    # Shorts-style subtitle settings
    # --------------------------------------------------------

    subtitle_filter = (
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
        "MarginV=80'"
    )

    # --------------------------------------------------------
    # FFmpeg command
    # --------------------------------------------------------

    command = [
        "ffmpeg",

        "-i",
        video_path,

        # ----------------------------------------------------
        # Burn styled subtitles
        # ----------------------------------------------------

        "-vf",
        subtitle_filter,

        # ----------------------------------------------------
        # Video
        # ----------------------------------------------------

        "-c:v",
        "libx264",

        "-preset",
        "medium",

        "-crf",
        "23",

        # ----------------------------------------------------
        # Audio
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
        # Overwrite
        # ----------------------------------------------------

        "-y",

        str(output_path)
    ]

    print("\n🎨 Burning styled captions...")
    print(f"📥 Video: {video_path}")
    print(f"📝 SRT:   {subtitle_path}")

    subprocess.run(
        command,
        check=True
    )

    print(
        f"✅ Styled captioned video created: "
        f"{output_path}"
    )

    return str(output_path)