from fastapi import FastAPI
from app.api.v1.router import router as api_v1_router

app = FastAPI(title="Vellora", version="1.0.0")

app.include_router(api_v1_router)

