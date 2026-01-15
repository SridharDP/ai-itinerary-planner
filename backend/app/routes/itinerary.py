import json
from fastapi import HTTPException
from fastapi import APIRouter, HTTPException
from app.models import ItineraryRequest, ItineraryResponse
from app.services.llm_service import call_llm
from app.utils.prompt_builder import build_itinerary_prompt
from app.utils.json_guard import safe_json_load
from app.services.place_service import (
    fetch_places,
    fetch_food_places,
    fetch_stay_areas
)


router = APIRouter(prefix="/itinerary", tags=["itinerary"])


def normalize_itinerary(itinerary: dict) -> dict:
    for day in itinerary.get("days", []):
        schedule = day.get("schedule", {})
        for slot in ["morning", "afternoon", "evening"]:
            cleaned = []
            for item in schedule.get(slot, []):
                if isinstance(item, dict):
                    cleaned.append(item.get("name", ""))
                else:
                    cleaned.append(item)
            schedule[slot] = cleaned

        food_cleaned = []
        for food in day.get("food", []):
            if isinstance(food, dict):
                food_cleaned.append(food.get("name", ""))
            else:
                food_cleaned.append(food)
        day["food"] = food_cleaned

    return itinerary


@router.post("/generate", response_model=ItineraryResponse)
def generate_itinerary(req: ItineraryRequest):

    try:
        destination = req.destination.lower()

        data = {
            "destination": destination.title(),
            "places": fetch_places(destination),
            "food": fetch_food_places(destination),
            "stay_areas": fetch_stay_areas(destination)
        }
    except RuntimeError:
        raise HTTPException(
        status_code=503,
        detail="Destination data temporarily unavailable. Please try again."
        )

    system_prompt = (
        "You are a strict JSON generator. "
        "Return valid JSON only."
    )

    user_prompt = build_itinerary_prompt(req.dict(), data)

    llm_output = call_llm(system_prompt, user_prompt)

    try:
        parsed = safe_json_load(llm_output)
    except Exception:
        retry_prompt = "Return ONLY valid JSON."
        llm_output = call_llm(retry_prompt, user_prompt)
        parsed = safe_json_load(llm_output)

    normalized = normalize_itinerary(parsed)
    return normalized
