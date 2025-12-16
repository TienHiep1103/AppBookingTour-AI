from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import ai_router
from .api import item_router
from .middlewares.exception_middleware import GlobalExceptionMiddleware

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