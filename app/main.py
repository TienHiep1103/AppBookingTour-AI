from fastapi import FastAPI
from .api import ai_router

app = FastAPI(title="AI Inference API")

app.include_router(ai_router.router)