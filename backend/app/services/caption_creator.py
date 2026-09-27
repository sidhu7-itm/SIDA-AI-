from pathlib import Path
import re


# ============================================================
# CREATE SHORTS-STYLE SRT
# ============================================================

def create_srt(
    transcript,
    clip_start: float,
    clip_end: float,
    subtitle_id: int
):

    output_folder = Path("subtitles")
    output_folder.mkdir(exist_ok=True)

    output_path = (
        output_folder /
        f"subtitle_{subtitle_id}.srt"
    )

    subtitle_blocks = []
    subtitle_number = 1

    # --------------------------------------------------------
    # Number of words per caption
    # --------------------------------------------------------

    WORDS_PER_CAPTION = 3

    # --------------------------------------------------------
    # Process Whisper segments
    # --------------------------------------------------------

    for segment in transcript:

        segment_start = float(segment["start"])
        segment_end = float(segment["end"])
        text = segment["text"].strip()

        if not text:
            continue

        # ----------------------------------------------------
        # Ignore segments outside the selected clip
        # ----------------------------------------------------

        if segment_end <= clip_start:
            continue

        if segment_start >= clip_end:
            continue

        # ----------------------------------------------------
        # Keep only the part inside the clip
        # ----------------------------------------------------

        actual_start = max(
            segment_start,
            clip_start
        )

        actual_end = min(
            segment_end,
            clip_end
        )

        if actual_end <= actual_start:
            continue

        # ----------------------------------------------------
        # Clean text
        # ----------------------------------------------------

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        # ----------------------------------------------------
        # Convert to uppercase
        # ----------------------------------------------------

        text = text.upper()

        # ----------------------------------------------------
        # Split into words
        # ----------------------------------------------------

        words = text.split()

        if not words:
            continue

        # ----------------------------------------------------
        # Divide the segment into small caption chunks
        # ----------------------------------------------------

        chunks = []

        for i in range(
            0,
            len(words),
            WORDS_PER_CAPTION
        ):

            chunk = words[
                i:i + WORDS_PER_CAPTION
            ]

            chunks.append(
                " ".join(chunk)
            )

        # ----------------------------------------------------
        # Calculate total duration
        # ----------------------------------------------------

        total_duration = (
            actual_end - actual_start
        )

        total_words = len(words)

        current_time = actual_start

        # ----------------------------------------------------
        # Give each caption time proportional to word count
        # ----------------------------------------------------

        for chunk in chunks:

            chunk_words = len(
                chunk.split()
            )

            chunk_duration = (
                total_duration
                * chunk_words
                / total_words
            )

            chunk_start = current_time

            chunk_end = (
                current_time
                + chunk_duration
            )

            # ------------------------------------------------
            # Convert original-video time
            # to clip-local time
            # ------------------------------------------------

            local_start = (
                chunk_start
                - clip_start
            )

            local_end = (
                chunk_end
                - clip_start
            )

            # ------------------------------------------------
            # Create SRT timestamps
            # ------------------------------------------------

            start_timestamp = (
                seconds_to_srt_time(
                    local_start
                )
            )

            end_timestamp = (
                seconds_to_srt_time(
                    local_end
                )
            )

            # ------------------------------------------------
            # Create subtitle block
            # ------------------------------------------------

            subtitle_blocks.append(
                f"{subtitle_number}\n"
                f"{start_timestamp} --> "
                f"{end_timestamp}\n"
                f"{chunk}\n"
            )

            subtitle_number += 1

            current_time = chunk_end

    # --------------------------------------------------------
    # Write SRT file
    # --------------------------------------------------------

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(subtitle_blocks)
        )

    print(
        f"📝 Shorts-style subtitle file created: "
        f"{output_path}"
    )

    return str(output_path)


# ============================================================
# CONVERT SECONDS → SRT TIME
# ============================================================

def seconds_to_srt_time(seconds: float):

    total_milliseconds = round(
        seconds * 1000
    )

    hours = (
        total_milliseconds
        // 3_600_000
    )

    remaining = (
        total_milliseconds
        % 3_600_000
    )

    minutes = (
        remaining
        // 60_000
    )

    remaining %= 60_000

    seconds_part = (
        remaining
        // 1000
    )

    milliseconds = (
        remaining
        % 1000
    )

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds_part:02d},"
        f"{milliseconds:03d}"
    )