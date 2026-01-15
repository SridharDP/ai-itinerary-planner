from app.services.db import get_db_connection
import logging

PLACES_CACHE = {}
FOOD_CACHE = {}
STAY_CACHE = {}


def fetch_places(destination: str):
    # 1️⃣ Cache first
    if destination in PLACES_CACHE:
        return PLACES_CACHE[destination]

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
              id,
              name,
              category,
              activity_type,
              best_time,
              time_required_hours,
              reusable,
              meta
            FROM places
            WHERE destination = %s
              AND is_active = true
            """,
            (destination,)
        )

        rows = cur.fetchall()
        conn.close()

        places = []
        for r in rows:
            place = {
                "id": r[0],
                "name": r[1],
                "category": r[2],
                "activity_type": r[3],
                "best_time": r[4],
                "time_required_hours": r[5],
                "reusable": r[6]
            }
            if r[7]:
                place.update(r[7])
            places.append(place)

        # 2️⃣ Populate cache on success
        PLACES_CACHE[destination] = places
        return places

    except Exception as e:
        logging.error(f"DB error fetching places for {destination}: {e}")

        # 3️⃣ Fallback to cache if exists
        if destination in PLACES_CACHE:
            return PLACES_CACHE[destination]

        # 4️⃣ No fallback available
        raise RuntimeError("Places data unavailable")
def fetch_food_places(destination: str):
    if destination in FOOD_CACHE:
        return FOOD_CACHE[destination]

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT name, best_time, near, food_type
            FROM food_places
            WHERE destination = %s
              AND is_active = true
            """,
            (destination,)
        )

        rows = cur.fetchall()
        conn.close()

        food = [
            {
                "name": r[0],
                "best_time": r[1],
                "near": r[2],
                "food_type": r[3]
            }
            for r in rows
        ]

        FOOD_CACHE[destination] = food
        return food

    except Exception as e:
        logging.error(f"DB error fetching food for {destination}: {e}")

        if destination in FOOD_CACHE:
            return FOOD_CACHE[destination]

        return []  # food is optional
def fetch_stay_areas(destination: str):
    if destination in STAY_CACHE:
        return STAY_CACHE[destination]

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT name, vibe
            FROM stay_areas
            WHERE destination = %s
              AND is_active = true
            """,
            (destination,)
        )

        rows = cur.fetchall()
        conn.close()

        stays = [{"name": r[0], "vibe": r[1]} for r in rows]

        STAY_CACHE[destination] = stays
        return stays

    except Exception as e:
        logging.error(f"DB error fetching stays for {destination}: {e}")

        if destination in STAY_CACHE:
            return STAY_CACHE[destination]

        return []
