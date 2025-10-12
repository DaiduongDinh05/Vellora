from uuid import UUID
from app.container import get_db
from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EndTripDTO, TripResponseDTO
from app.modules.trips.service import TripsService
from app.modules.trips.exceptions import InvalidTripDataError, TripAlreadyActiveError, TripNotFoundError, TripPersistenceError
from fastapi import APIRouter, Depends, HTTPException
from app.infra.db import AsyncSession


router = APIRouter(prefix="/trips")

def get_trips_service(db: AsyncSession = Depends(get_db)):
    return TripsService(TripRepo(db))

@router.post("/", response_model = TripResponseDTO)
async def start_trip(body: CreateTripDTO, svc: TripsService = Depends(get_trips_service)):
    try:
        trip = await svc.start_trip(body)
        return TripResponseDTO.model_validate(trip)
    
    except InvalidTripDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TripAlreadyActiveError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TripPersistenceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
@router.patch("/{trip_id}/end", response_model=TripResponseDTO)
async def end_trip(trip_id: UUID, body: EndTripDTO, svc: TripsService = Depends(get_trips_service)):
    try:
        trip = await svc.end_trip(trip_id, body)
        return TripResponseDTO.model_validate(trip)
    
    except InvalidTripDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TripPersistenceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TripNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error")

