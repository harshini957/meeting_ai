import os
import json
from deepgram import DeepgramClient, PrerecordedOptions, FileSource

# -------------------------------------------------
# Batch transcription (Deepgram SDK v4.8.0)
# -------------------------------------------------
def transcribe_audio_file(local_audio_path: str) -> dict:
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPGRAM_API_KEY not found in environment")

    client = DeepgramClient(api_key)

    with open(local_audio_path, "rb") as audio:
        buffer_data = audio.read()

    payload: FileSource = {
        "buffer": buffer_data,
    }

    options = PrerecordedOptions(
        model="nova-2",
        diarize=True,
        punctuate=True,
        smart_format=True,
        utterances=True,
    )

    # Correct API call for SDK v4
    response = client.listen.rest.v("1").transcribe_file(payload, options)

    # Convert response to dict if it's a Pydantic model
    if hasattr(response, 'to_dict'):
        return response.to_dict()
    elif hasattr(response, 'model_dump'):
        return response.model_dump()
    else:
        return response


# -------------------------------------------------
# Save full Deepgram response as JSON
# -------------------------------------------------
def save_transcript_json(response: dict, meeting_id: str) -> str:
    os.makedirs("data/transcripts/raw", exist_ok=True)
    path = f"data/transcripts/raw/meeting_{meeting_id}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2)

    return path


# -------------------------------------------------
# Extract readable speaker-based transcript
# -------------------------------------------------
def extract_readable_transcript(response: dict) -> str:
    results = response.get("results", {})
    utterances = results.get("utterances", [])

    if not utterances:
        return "No speech detected."

    lines = []
    for u in utterances:
        speaker = u.get("speaker", "Unknown")
        transcript = u.get("transcript", "")
        lines.append(f"Speaker {speaker}: {transcript}")

    return "\n".join(lines)


# -------------------------------------------------
# Save readable transcript text
# -------------------------------------------------
def save_transcript_text(text: str, meeting_id: str) -> str:
    os.makedirs("data/transcripts/text", exist_ok=True)
    path = f"data/transcripts/text/meeting_{meeting_id}.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path