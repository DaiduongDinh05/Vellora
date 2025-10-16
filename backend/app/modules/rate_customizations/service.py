from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.schemas import CreateRateCustomizationDTO
from app.modules.rate_customizations.exceptions import InvalidRateCustomizationDataError, RateCustomizationPersistenceError
from app.modules.rate_customizations.models import RateCustomization


class RateCustomizationsService:
    def __init__(self, repo: RateCustomizationRepo):
        self.repo = repo

    async def create_rate_customization(self, data: CreateRateCustomizationDTO):
        if not data.name.strip():
            raise InvalidRateCustomizationDataError("Name is required")
        
        if not data.year:
            raise InvalidRateCustomizationDataError("Year is required")
        
        #once user is implemented add this and other checks
        # existing = await self.repo.get_by_name_and_user(name=body.name, user_id=user_id)
        # if existing:    
        #     raise DuplicateRateCustomizationError(status_code=400, detail="Rate customization name already exists for this user")
        
        try:
            rate_customization = RateCustomization(
                name = data.name,
                description = data.description,
                year = data.year 
            )

            return await self.repo.save_customization(rate_customization)
        
        except Exception as e:
            raise RateCustomizationPersistenceError("Unexpected error occured while saving customziation") from e