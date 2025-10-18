from uuid import UUID
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.schemas import CreateRateCustomizationDTO, EditRateCustomizationDTO
from app.modules.rate_customizations.exceptions import InvalidRateCustomizationDataError, RateCustomizationPersistenceError, RateCustomizationNotFoundError
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

            return await self.repo.save(rate_customization)
        
        except Exception as e:
            raise RateCustomizationPersistenceError("Unexpected error occured while saving customziation") from e
        
    async def get_customization(self, customization_id : UUID):
        rate_customization = await self.repo.get_customization(customization_id)

        if not rate_customization:
            raise RateCustomizationNotFoundError("Customization not found.")
        
        return rate_customization
    
    async def edit_customization(self, customization_id : UUID, data: EditRateCustomizationDTO):
        rate_customization = await self.get_customization(customization_id)

        if data.name is not None:
            if not data.name.strip():
                raise InvalidRateCustomizationDataError("name cannot be empty")
            rate_customization.name = data.name.strip()

        if data.description is not None:
            rate_customization.description = data.description

        if data.year is not None:
            if not data.year:
                raise InvalidRateCustomizationDataError("Year is required")
        
        return await self.repo.save(rate_customization)
