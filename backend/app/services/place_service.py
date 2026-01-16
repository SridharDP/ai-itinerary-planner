from app.services.supabase_client import supabase
import logging
logger = logging.getLogger(__name__)



def fetch_places(destination: str):
    res = (
        supabase
        .table("places")
        .select("*")
        .eq("destination", destination)
        .execute()
    )

    if not res.data:
        raise Exception("Places data unavailable")

    return res.data
logger.info("Fetching places")

def fetch_food_places(destination: str):
    logger.info("Fetching food_places from Supabase")
    res = (
        supabase
        .table("food_places")
        .select("*")
        .eq("destination", destination)
        .execute()
    )
    return res.data or []
logger.info("Fetching food places")


def fetch_stay_areas(destination: str):
    res = (
        supabase
        .table("stay_areas")
        .select("*")
        .eq("destination", destination)
        .execute()
    )

    return res.data or []
logger.info("Fetching stay areas")
