from uuid import UUID
from app.container import get_db
from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EndTripDTO, TripResponseDTO
from app.modules.trips.service import TripsService
from app.modules.trips.utils.error_handler  import error_handler
from fastapi import APIRouter, Depends
from app.infra.db import AsyncSession


router = APIRouter(prefix="/trips")

def get_trips_service(db: AsyncSession = Depends(get_db)):
    return TripsService(TripRepo(db))

@router.post("/", response_model = TripResponseDTO)
@error_handler
async def start_trip(body: CreateTripDTO, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.start_trip(body)
    return TripResponseDTO.model_validate(trip)

    
@router.patch("/{trip_id}/end", response_model=TripResponseDTO)
@error_handler
async def end_trip(trip_id: UUID, body: EndTripDTO, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.end_trip(trip_id, body)
    return TripResponseDTO.model_validate(trip)
    
@router.get("/{trip_id}", response_model=TripResponseDTO)
@error_handler
async def get_trip(trip_id: UUID, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.get_trip_by_id(trip_id)
    return TripResponseDTO.model_validate(trip)