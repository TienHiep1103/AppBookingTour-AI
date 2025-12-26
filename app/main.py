from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import ai_router
from .api import item_router
from app.middlewares.exception_middleware import GlobalExceptionMiddleware
from app.db import SessionLocal
from app.services.ai.cf_train_service import train_cf_models

app = FastAPI(title="AI Inference API")
app.add_middleware(GlobalExceptionMiddleware)
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(ai_router.router)
app.include_router(item_router.router)

@app.get("/")
def read_root():
    return "Hello AI API"

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        print("🚀 Training CF models on startup...")
        train_cf_models(db)
        print("✅ CF models trained successfully")
    except Exception as e:
        print("❌ CF training failed:", e)
    finally:
        db.close()