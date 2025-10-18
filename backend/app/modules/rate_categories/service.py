from uuid import UUID
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_categories.schemas import CreateRateCategoryDTO, EditRateCategoryDTO
from app.modules.rate_categories.exceptions import InvalidRateCategoryDataError, RateCategoryPersistenceError, RateCategoryNotFoundError
from app.modules.rate_categories.models import RateCategory
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.exceptions import RateCustomizationNotFoundError


class RateCategoriesService:
    def __init__(self, category_repo: RateCategoryRepo, customization_repo: RateCustomizationRepo):
        self.category_repo = category_repo
        self.customization_repo = customization_repo

    async def create_rate_category(self, customization_id: UUID,  data: CreateRateCategoryDTO):

        rate_customization = await self.customization_repo.get(customization_id)

        if not rate_customization:
            raise RateCustomizationNotFoundError("Customization not found.")

        if not data.name.strip():
            raise InvalidRateCategoryDataError("Name is required")
        
        if data.cost_per_mile is None or data.cost_per_mile <= 0:
            raise InvalidRateCategoryDataError("Cost per mile must be a non-negative number")

        try:
            rate_category = RateCategory(
                name=data.name.strip(),
                cost_per_mile=data.cost_per_mile,
                rate_customization_id=customization_id
            )

            return await self.category_repo.save(rate_category)

        except Exception as e:
            raise RateCategoryPersistenceError("Unexpected error occurred while saving rate category") from e
        
    async def get_category(self, category_id : UUID):
        rate_category = await self.category_repo.get(category_id)

        if not rate_category:
            raise RateCategoryNotFoundError("category not found.")
        
        return rate_category
    
    async def get_categories_by_customization(self, customization_id: UUID):
        rate_customization = await self.customization_repo.get(customization_id)

        if not rate_customization:
            raise RateCustomizationNotFoundError("Customization not found.")

        try:
            categories = await self.category_repo.get_by_customization_id(customization_id)
            return categories
        except Exception as e:
            raise RateCategoryPersistenceError("Unexpected error occurred while fetching categories") from e
    
    async def edit_category(self, category_id : UUID, data: EditRateCategoryDTO):
        rate_category = await self.get_category(category_id)

        if data.name is not None:
            if not data.name.strip():
                raise InvalidRateCategoryDataError("Name cannot be empty")
            rate_category.name = data.name.strip()

        if data.cost_per_mile is not None:
            if data.cost_per_mile <= 0:
                raise InvalidRateCategoryDataError("Cost per mile must be a non-negative number")
            rate_category.cost_per_mile = data.cost_per_mile

        try:
            return await self.category_repo.save(rate_category)
        except Exception as e:
            raise RateCategoryPersistenceError("Unexpected error occurred while updating rate category") from e
    
    async def delete_category(self, category_id: UUID):
        rate_category = await self.get_category(category_id)
        return await self.category_repo.delete(rate_category)
