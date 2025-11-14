from uuid import UUID
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.schemas import CreateRateCustomizationDTO, EditRateCustomizationDTO
from app.modules.rate_customizations.exceptions import InvalidRateCustomizationDataError, RateCustomizationPersistenceError, RateCustomizationNotFoundError
from app.modules.rate_customizations.exceptions import DuplicateRateCustomizationError
from app.modules.rate_customizations.models import RateCustomization
from sqlalchemy.exc import IntegrityError


class RateCustomizationsService:
    def __init__(self, repo: RateCustomizationRepo):
        self.repo = repo

    async def create_rate_customization(self, user_id: UUID, data: CreateRateCustomizationDTO):
        if not data.name.strip():
            raise InvalidRateCustomizationDataError("Name is required")
        
        if not data.year:
            raise InvalidRateCustomizationDataError("Year is required")
        
        cleaned_name = data.name.strip()
        existing = await self.repo.get_by_user_and_name(user_id, cleaned_name)
        if existing:
            raise DuplicateRateCustomizationError("A rate customization with this name already exists for this user")
        
        try:
            rate_customization = RateCustomization(
                user_id=user_id,
                name = cleaned_name,
                description = data.description,
                year = data.year 
            )

            return await self.repo.save(rate_customization)
        except Exception as e:
            raise RateCustomizationPersistenceError("Unexpected error occured while saving customziation") from e
        
    async def get_customization(self, user_id: UUID, customization_id : UUID):
        rate_customization = await self.repo.get(customization_id, user_id=user_id)

        if not rate_customization:
            #if not found check if its an IRS customization
            if await self.repo.is_irs_customization(customization_id):
                rate_customization = await self.repo.get(customization_id)

        if not rate_customization:
            raise RateCustomizationNotFoundError("Customization not found.")
        
        return rate_customization

    async def get_user_customizations(self, user_id: UUID):
        return await self.repo.get_user_customizations(user_id)
    
    async def edit_customization(self, user_id: UUID, customization_id : UUID, data: EditRateCustomizationDTO):
        customization = await self.get_customization(user_id, customization_id)
        
        if await self.repo.is_irs_customization(customization_id):
            raise InvalidRateCustomizationDataError("IRS standard rates cannot be modified")

        if data.name is not None:
            if not data.name.strip():
                raise InvalidRateCustomizationDataError("name cannot be empty")
            
            cleaned_name = data.name.strip()
            if cleaned_name != customization.name:
                existing = await self.repo.get_by_user_and_name(user_id, cleaned_name)
                if existing:
                    raise DuplicateRateCustomizationError("A rate customization with this name already exists for this user")
            customization.name = cleaned_name

        if data.description is not None:
            customization.description = data.description

        if data.year is not None:
            if not data.year:
                raise InvalidRateCustomizationDataError("Year is required")
            customization.year = data.year
        
        return await self.repo.save(customization)
    
    async def delete_customization(self, user_id: UUID, customization_id: UUID):
        customization = await self.get_customization(user_id, customization_id)
        
        if await self.repo.is_irs_customization(customization_id):
            raise InvalidRateCustomizationDataError("IRS standard rates cannot be deleted")
            
        return await self.repo.delete(customization)

