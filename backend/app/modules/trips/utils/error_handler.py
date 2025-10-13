
from functools import wraps
from app.modules.trips.exceptions import InvalidTripDataError, TripAlreadyActiveError, TripNotFoundError, TripPersistenceError
from fastapi import HTTPException

def error_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except InvalidTripDataError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except TripAlreadyActiveError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except TripPersistenceError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except TripNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Unexpected server error")
        
    return wrapper