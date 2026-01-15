import json
import re


def safe_json_load(text: str) -> dict:
    """
    Tries to safely extract and parse JSON from LLM output.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try extracting JSON block using regex
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group())
        raise
