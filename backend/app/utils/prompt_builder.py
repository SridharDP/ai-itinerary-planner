import json


def build_itinerary_prompt(req: dict, hampi_data: dict) -> str:
    return f"""
You are a local travel itinerary planner for Hampi, India.

STRICT RULES:
- Use ONLY the provided data
- Do NOT invent places
- Do NOT add explanations
- Return ONLY valid JSON
- For schedules and food, return ONLY the PLACE NAME as a string
- Never return full objects, ids, or metadata
If unique places are insufficient:
- Use filler activities (walks, scenic time, rest, food)
- Reuse reusable activities if needed
- Do NOT invent new place names




DESTINATION DATA:
{json.dumps(hampi_data, indent=2)}

USER INPUT:
{json.dumps(req, indent=2)}

OUTPUT SCHEMA:
{{
  "destination": "Hampi",
  "days": [
    {{
      "day": 1,
      "schedule": {{
        "morning": [],
        "afternoon": [],
        "evening": []
      }},
      "food": [],
      "stay_area": "",
      "commute_tips": ""
    }}
  ]
}}
"""
