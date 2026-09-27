import json
import os

from google import genai


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# GEMINI CLIENT
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "❌ GEMINI_API_KEY is not set.\n\n"
        "Set it in PowerShell with:\n"
        '$env:GEMINI_API_KEY="YOUR_API_KEY"'
    )

client = genai.Client(api_key=api_key)


# ============================================================
# STRUCTURED OUTPUT SCHEMA
# ============================================================

OUTPUT_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "start": {
                "type": "number",
                "description": "Start time in seconds."
            },
            "end": {
                "type": "number",
                "description": "End time in seconds."
            },
            "reason": {
                "type": "string",
                "description": (
                    "Brief explanation of why this moment "
                    "would make an engaging YouTube Short."
                )
            }
        },
        "required": [
            "start",
            "end",
            "reason"
        ]
    }
}


# ============================================================
# ASK GEMINI
# ============================================================

def ask_gemini(prompt: str):

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": OUTPUT_SCHEMA
        }
    )

    return interaction.output_text.strip()


# ============================================================
# VALIDATE MOMENTS
# ============================================================

def validate_moments(result, transcript):

    if not isinstance(result, list):
        print("❌ Gemini response is not a list.")
        return []

    if not transcript:
        print("❌ Transcript is empty.")
        return []

    # --------------------------------------------------------
    # Get actual transcript boundaries
    # --------------------------------------------------------

    transcript_start = min(
        float(segment["start"])
        for segment in transcript
        if "start" in segment
    )

    transcript_end = max(
        float(segment["end"])
        for segment in transcript
        if "end" in segment
    )

    valid_moments = []

    # --------------------------------------------------------
    # Validate each selected moment
    # --------------------------------------------------------

    for moment in result:

        if not isinstance(moment, dict):
            print("⚠️ Skipping invalid moment.")
            continue

        if "start" not in moment or "end" not in moment:
            print("⚠️ Skipping moment without timestamps.")
            continue

        try:
            start = float(moment["start"])
            end = float(moment["end"])
        except (TypeError, ValueError):
            print("⚠️ Skipping moment with invalid timestamps.")
            continue

        reason = str(
            moment.get("reason", "")
        ).strip()

        # ----------------------------------------------------
        # Timestamp boundaries
        # ----------------------------------------------------

        if start < transcript_start:
            print(
                f"⚠️ Start {start} is before transcript."
            )
            continue

        if end > transcript_end:
            print(
                f"⚠️ End {end} is after transcript."
            )
            continue

        # ----------------------------------------------------
        # Timestamp order
        # ----------------------------------------------------

        if end <= start:
            print(
                f"⚠️ Invalid range: "
                f"{start} → {end}"
            )
            continue

        # ----------------------------------------------------
        # Duration
        # ----------------------------------------------------

        duration = end - start

        if duration < 20:
            print(
                f"⚠️ Skipping short moment: "
                f"{start} → {end} "
                f"({duration:.1f}s)"
            )
            continue

        if duration > 60:
            print(
                f"⚠️ Skipping long moment: "
                f"{start} → {end} "
                f"({duration:.1f}s)"
            )
            continue

        valid_moments.append(
            {
                "start": start,
                "end": end,
                "reason": reason
            }
        )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    unique_moments = []

    seen = set()

    for moment in valid_moments:

        key = (
            moment["start"],
            moment["end"]
        )

        if key not in seen:

            seen.add(key)
            unique_moments.append(moment)

    # Maximum 5 clips
    unique_moments = unique_moments[:5]

    return unique_moments


# ============================================================
# MAIN SELECTOR
# ============================================================

def select_moments(transcript):

    transcript_text = json.dumps(
        transcript,
        indent=2
    )

    prompt = f"""
You are an expert editor for YouTube Shorts.

Analyze the REAL timestamped video transcript below.

Find the strongest moments that could become engaging
YouTube Shorts.

Look for:

- strong hooks
- surprising information
- curiosity
- emotion
- humor
- controversy
- interesting stories
- strong statements
- twists
- memorable lines
- moments that make viewers want to keep watching

IMPORTANT RULES:

1. Select only genuinely interesting moments.
2. Do NOT select every transcript segment.
3. A moment may contain multiple transcript segments.
4. Each moment MUST be between 20 and 60 seconds.
5. Use timestamps from the REAL transcript.
6. Do NOT invent timestamps outside the transcript.
7. Prefer natural, complete sections.
8. Select the best 1 to 5 moments.
9. Quality is more important than quantity.
10. Return ONLY the JSON array.
11. Every item MUST contain:
    start
    end
    reason
12. start and end MUST be numbers.
13. reason MUST briefly explain why the moment is engaging.

REAL TRANSCRIPT:

{transcript_text}
"""

    print("\n🤖 Sending REAL transcript to Gemini 3.6 Flash...")

    try:

        content = ask_gemini(prompt)

    except Exception as error:

        print("\n❌ Gemini API error:")
        print(error)

        return []

    print("\nRAW GEMINI RESPONSE:")
    print(content)

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        result = json.loads(content)

    except json.JSONDecodeError:

        print("❌ Gemini returned invalid JSON.")
        return []

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    valid_moments = validate_moments(
        result,
        transcript
    )

    if not valid_moments:

        print(
            "\n❌ Gemini did not return any valid moments."
        )

        return []

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print(
        f"\n✅ Validated "
        f"{len(valid_moments)} "
        f"Gemini-selected moment(s)."
    )

    return valid_moments