from fastapi import APIRouter
from app.modules.trips.router import router as trips_router
from app.modules.expenses.router import router as expenses_router

router = APIRouter(prefix="/api/v1")

router.include_router(trips_router)
router.include_router(expenses_router)
