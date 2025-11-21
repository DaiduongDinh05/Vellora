from uuid import UUID
from app.container import get_db
from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO, TripResponseDTO, ManualCreateTripDTO
from app.modules.trips.service import TripsService
from app.core.error_handler  import error_handler
from app.core.dependencies import get_current_user
from app.modules.users.models import User
from fastapi import APIRouter, Depends
from app.infra.db import AsyncSession
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.expenses.repository import ExpenseRepo
from app.modules.expenses.service import ExpensesService


router = APIRouter(prefix="/trips", tags=["Trips"])

def get_trips_service(db: AsyncSession = Depends(get_db)):
    trip_repo = TripRepo(db)
    expense_repo = ExpenseRepo(db)
    expense_service = ExpensesService(expense_repo, trip_repo)
    return TripsService(trip_repo, RateCategoryRepo(db), RateCustomizationRepo(db), expense_service)

@router.post("/", response_model = TripResponseDTO)
@error_handler
async def start_trip(body: CreateTripDTO, svc: TripsService = Depends(get_trips_service), current_user: User = Depends(get_current_user)):
    trip = await svc.start_trip(current_user.id, body)
    return TripResponseDTO.model_validate(trip)

@router.post("/manual", response_model = TripResponseDTO)
@error_handler
async def manual_create_trip(body: ManualCreateTripDTO, svc: TripsService = Depends(get_trips_service), current_user: User = Depends(get_current_user)):
    trip = await svc.manual_create_trip(current_user.id, body)
    return TripResponseDTO.model_validate(trip)

@router.patch("/{trip_id}", response_model=TripResponseDTO)
@error_handler
async def edit_trip(trip_id: UUID, body: EditTripDTO, svc: TripsService = Depends(get_trips_service), current_user: User = Depends(get_current_user)):
    trip = await svc.edit_trip(current_user.id, trip_id, body)
    return TripResponseDTO.model_validate(trip)
   
@router.patch("/{trip_id}/end", response_model=TripResponseDTO)
@error_handler
async def end_trip(trip_id: UUID, body: EndTripDTO, svc: TripsService = Depends(get_trips_service), current_user: User = Depends(get_current_user)):
    trip = await svc.end_trip(current_user.id, trip_id, body)
    return TripResponseDTO.model_validate(trip)

@router.patch("/{trip_id}/cancel", response_model=TripResponseDTO)
@error_handler
async def cancel_trip(trip_id: UUID, svc: TripsService = Depends(get_trips_service), current_user: User = Depends(get_current_user)):
    trip = await svc.cancel_trip(current_user.id, trip_id)
    return TripResponseDTO.model_validate(trip)
    
@router.get("/active", response_model=TripResponseDTO)
@error_handler
async def get_active_trip(svc: TripsService = Depends(get_trips_service), current_user: User = Depends(get_current_user)):
    trip = await svc.get_active_trip(current_user.id)
    if not trip:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active trip found")
    return TripResponseDTO.model_validate(trip)

@router.get("/{trip_id}", response_model=TripResponseDTO)
@error_handler
async def get_trip(trip_id: UUID, svc: TripsService = Depends(get_trips_service), current_user: User = Depends(get_current_user)):
    trip = await svc.get_trip_by_id(current_user.id, trip_id)
    return TripResponseDTO.model_validate(trip)

@router.get("/", response_model=list[TripResponseDTO])
@error_handler
async def get_user_trips(svc: TripsService = Depends(get_trips_service), current_user: User = Depends(get_current_user)):
    trips = await svc.get_trips_by_userId(current_user.id)
    return [TripResponseDTO.model_validate(trip) for trip in trips]

