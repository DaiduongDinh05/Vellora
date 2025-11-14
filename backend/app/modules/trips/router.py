from uuid import UUID
from app.container import get_db
from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO, TripResponseDTO, ManualCreateTripDTO
from app.modules.trips.service import TripsService
from app.core.error_handler  import error_handler
from fastapi import APIRouter, Depends
from app.infra.db import AsyncSession
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.expenses.repository import ExpenseRepo
from app.modules.expenses.service import ExpensesService


router = APIRouter(prefix="/trips", tags=["Trips"]) #will insert userid once implemented as this should live under users

def get_trips_service(db: AsyncSession = Depends(get_db)):
    trip_repo = TripRepo(db)
    expense_repo = ExpenseRepo(db)
    expense_service = ExpensesService(expense_repo, trip_repo)
    return TripsService(trip_repo, RateCategoryRepo(db), RateCustomizationRepo(db), expense_service)

@router.post("/", response_model = TripResponseDTO)
@error_handler
async def start_trip(body: CreateTripDTO, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.start_trip(body)
    return TripResponseDTO.model_validate(trip)

@router.post("/manual", response_model = TripResponseDTO)
@error_handler
async def manual_create_trip(body: ManualCreateTripDTO, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.manual_create_trip(body)
    return TripResponseDTO.model_validate(trip)

@router.patch("/{trip_id}", response_model=TripResponseDTO)
@error_handler
async def edit_trip(trip_id: UUID, body: EditTripDTO, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.edit_trip(trip_id, body)
    return TripResponseDTO.model_validate(trip)
   
@router.patch("/{trip_id}/end", response_model=TripResponseDTO)
@error_handler
async def end_trip(trip_id: UUID, body: EndTripDTO, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.end_trip(trip_id, body)
    return TripResponseDTO.model_validate(trip)

@router.patch("/{trip_id}/cancel", response_model=TripResponseDTO)
@error_handler
async def cancel_trip(trip_id: UUID, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.cancel_trip(trip_id)
    return TripResponseDTO.model_validate(trip)
    
@router.get("/{trip_id}", response_model=TripResponseDTO)
@error_handler
async def get_trip(trip_id: UUID, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.get_trip_by_id(trip_id)
    return TripResponseDTO.model_validate(trip)

