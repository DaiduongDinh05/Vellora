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

    #will add user id here later
    async def create_rate_customization(self, data: CreateRateCustomizationDTO):
        if not data.name.strip():
            raise InvalidRateCustomizationDataError("Name is required")
        
        if not data.year:
            raise InvalidRateCustomizationDataError("Year is required")
        
        #for when user id is implemented
        # cleaned_name = data.name.strip()
        # existing = await self.repo.get_by_user_and_name(user_id, cleaned_name)
        # if existing:
        #     raise DuplicateRateCustomizationError("A rate customization with this name already exists for this user")
        
        try:
            rate_customization = RateCustomization(
                name = data.name,
                #for when user is added
                # user_id = user_id,
                # name = cleaned_name,
                description = data.description,
                year = data.year 
            )

            return await self.repo.save(rate_customization)
        #for when user is implemented
        # except IntegrityError as e:
        #     raise DuplicateRateCustomizationError("A rate customization with this name already exists for this user") from e
        except Exception as e:
            raise RateCustomizationPersistenceError("Unexpected error occured while saving customziation") from e
        
    async def get_customization(self, customization_id : UUID):
        rate_customization = await self.repo.get(customization_id)

        if not rate_customization:
            raise RateCustomizationNotFoundError("Customization not found.")
        
        return rate_customization
    
    async def edit_customization(self, customization_id : UUID, data: EditRateCustomizationDTO):
        rate_customization = await self.get_customization(customization_id)

        if data.name is not None:
            if not data.name.strip():
                raise InvalidRateCustomizationDataError("name cannot be empty")
            rate_customization.name = data.name.strip()

            #for when user is added
            # cleaned_name = data.name.strip()
            # if cleaned_name != rate_customization.name:
            #     existing = await self.repo.get_by_user_and_name(rate_customization.user_id, cleaned_name)
            #     if existing:
            #         raise DuplicateRateCustomizationError("A rate customization with this name already exists for this user")
            # rate_customization.name = cleaned_name

        if data.description is not None:
            rate_customization.description = data.description

        if data.year is not None:
            if not data.year:
                raise InvalidRateCustomizationDataError("Year is required")
        
        return await self.repo.save(rate_customization)
    
    async def delete_customization(self, customziation_id: UUID):
        rate_customization = await self.get_customization(customziation_id)
        return await self.repo.delete(rate_customization)
