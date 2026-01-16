import json
import logging
from fastapi import APIRouter, HTTPException

from app.models import ItineraryRequest, ItineraryResponse
from app.services.llm_service import call_llm
from app.utils.prompt_builder import build_itinerary_prompt
from app.utils.json_guard import safe_json_load
from app.services.place_service import (
    fetch_places,
    fetch_food_places,
    fetch_stay_areas,
)
from app.cache import cache  # in-memory cache

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/itinerary", tags=["itinerary"])


def normalize_itinerary(itinerary: dict) -> dict:
    for day in itinerary.get("days", []):
        schedule = day.get("schedule", {})

        for slot in ["morning", "afternoon", "evening"]:
            schedule[slot] = [
                item["name"] if isinstance(item, dict) else item
                for item in schedule.get(slot, [])
            ]

        day["food"] = [
            food["name"] if isinstance(food, dict) else food
            for food in day.get("food", [])
        ]

    return itinerary


@router.post("/generate", response_model=ItineraryResponse)
def generate_itinerary(req: ItineraryRequest):
    destination = req.destination.lower()

    # 1️⃣ Fetch data (DB → cache fallback)
    try:
        places = fetch_places(destination)
        food = fetch_food_places(destination)
        stays = fetch_stay_areas(destination)

        cache[destination] = {
            "places": places,
            "food": food,
            "stays": stays,
        }

    except Exception as e:
        logger.error(f"DB error fetching data for {destination}: {e}")
        cached = cache.get(destination)

        if not cached:
            raise HTTPException(
                status_code=503,
                detail="Data is waking up. Please try again in a moment."
            )

        places = cached["places"]
        food = cached["food"]
        stays = cached["stays"]

    data = {
        "destination": destination,
        "places": places,
        "food": food,
        "stay_areas": stays,
    }

    # 2️⃣ Build prompt
    system_prompt = (
        "You are a strict JSON generator. "
        "Return valid JSON only. No explanations."
    )

    user_prompt = build_itinerary_prompt(req.dict(), data)

    # 3️⃣ Call LLM with retry
    try:
        llm_output = call_llm(system_prompt, user_prompt)
        parsed = safe_json_load(llm_output)

    except Exception:
        retry_prompt = "Return ONLY valid JSON. No text."
        llm_output = call_llm(retry_prompt, user_prompt)
        parsed = safe_json_load(llm_output)

    # 4️⃣ Normalize & return
    return normalize_itinerary(parsed)
