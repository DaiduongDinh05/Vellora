from uuid import UUID
from app.container import get_db
from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO, TripResponseDTO
from app.modules.trips.service import TripsService
from app.core.error_handler  import error_handler
from fastapi import APIRouter, Depends
from app.infra.db import AsyncSession


router = APIRouter(prefix="/trips") #will insert userid once implemented as this should live under users

def get_trips_service(db: AsyncSession = Depends(get_db)):
    return TripsService(TripRepo(db))

@router.post("/", response_model = TripResponseDTO)
@error_handler
async def start_trip(body: CreateTripDTO, svc: TripsService = Depends(get_trips_service)):
    trip = await svc.start_trip(body)
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

