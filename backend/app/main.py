from fastapi import FastAPI
from app.routes.itinerary import router as itinerary_router

app = FastAPI(
    title="AI Itinerary Planner",
    description="LLM-powered local itinerary planner",
    version="0.1.0"
)

app.include_router(itinerary_router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Itinerary Planner backend is running"}
