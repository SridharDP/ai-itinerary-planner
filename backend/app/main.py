from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.itinerary import router as itinerary_router
from dotenv import load_dotenv
load_dotenv()

# 1️⃣ Create app FIRST
app = FastAPI(
    title="AI Itinerary Planner",
    description="LLM-powered local itinerary planner",
    version="0.1.0"
)

# 2️⃣ Add middleware AFTER app exists
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Include routers
app.include_router(itinerary_router)

# 4️⃣ Health check
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "AI Itinerary Planner backend is running"
    }
