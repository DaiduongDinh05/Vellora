from fastapi import APIRouter
from app.modules.trips.router import router as trips_router

router = APIRouter(prefix="/api/v1")

router.include_router(trips_router)
