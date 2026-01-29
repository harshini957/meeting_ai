import os
import json
from google import genai
from google.genai import types  # Add this import at the top
# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "models/gemini-2.5-flash"  # correct, supported model


# def extract_action_items(transcript_text: str) -> dict:
#     prompt = f"""
# You are a system that extracts meeting action items.
#
# Rules:
# - Return ONLY valid JSON
# - Do NOT add explanations
# - Do NOT invent people
# - If unclear, set value to null
#
# Output format:
# {{
#   "action_items": [
#     {{
#       "task": string,
#       "owner": string | null,
#       "assigned_by": string | null,
#       "due_date": string | null,
#       "source_sentence": string
#     }}
#   ]
# }}
#
# Transcript:
# \"\"\"
# {transcript_text}
# \"\"\"
# """
#
#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt
#     )
#
#     return json.loads(response.text)




def extract_action_items(transcript_text: str) -> dict:
    prompt = f"Extract meeting action items from this transcript: {transcript_text}"

    # Use config to force JSON output
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a system that extracts meeting action items. Return a valid JSON.",
            response_mime_type="application/json",
            # This 'response_schema' ensures the JSON matches your exact format
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "action_items": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "task": {"type": "STRING"},
                                "owner": {"type": "STRING"},
                                "assigned_by": {"type": "STRING"},
                                "due_date": {"type": "STRING"},
                                "source_sentence": {"type": "STRING"}
                            }
                        }
                    }
                }
            }
        )
    )

    # With response_mime_type, you can safely load the response directly
    return json.loads(response.text)


def save_action_items(action_data: dict, meeting_id: str) -> str:
    os.makedirs("data/action_items", exist_ok=True)
    path = f"data/action_items/meeting_{meeting_id}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(action_data, f, indent=2)

    return path
