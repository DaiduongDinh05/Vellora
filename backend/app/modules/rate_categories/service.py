from uuid import UUID
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_categories.schemas import CreateRateCategoryDTO, EditRateCategoryDTO
from app.modules.rate_categories.exceptions import InvalidRateCategoryDataError, RateCategoryPersistenceError, RateCategoryNotFoundError
from app.modules.rate_categories.exceptions import DuplicateRateCategoryError
from app.modules.rate_categories.models import RateCategory
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.exceptions import RateCustomizationNotFoundError
from sqlalchemy.exc import IntegrityError


class RateCategoriesService:
    def __init__(self, category_repo: RateCategoryRepo, customization_repo: RateCustomizationRepo):
        self.category_repo = category_repo
        self.customization_repo = customization_repo

    async def create_rate_category(self, user_id: UUID, customization_id: UUID, data: CreateRateCategoryDTO):
        
        if await self.customization_repo.is_irs_customization(customization_id):
            raise InvalidRateCategoryDataError("Cannot add categories to IRS standard rates")

        rate_customization = await self.customization_repo.get(customization_id, user_id)

        if not rate_customization:
            raise RateCustomizationNotFoundError("Customization not found or not owned by user.")

        if not data.name.strip():
            raise InvalidRateCategoryDataError("Name is required")
        
        if data.cost_per_mile is None or data.cost_per_mile <= 0:
            raise InvalidRateCategoryDataError("Cost per mile must be a non-negative number")

        cleaned_name = data.name.strip()
        existing = await self.category_repo.get_by_customization_and_name(customization_id, cleaned_name)
        if existing:
            raise DuplicateRateCategoryError("A rate category with this name already exists for this customization")

        try:
            rate_category = RateCategory(
                name=cleaned_name,
                cost_per_mile=data.cost_per_mile,
                rate_customization_id=customization_id
            )

            return await self.category_repo.save(rate_category)
        except IntegrityError as e:
            raise DuplicateRateCategoryError("A rate category with this name already exists for this customization") from e
        except Exception as e:
            raise RateCategoryPersistenceError("Unexpected error occurred while saving rate category") from e
        
    async def get_category(self, user_id: UUID, category_id: UUID):
        rate_category = await self.category_repo.get(category_id)

        if not rate_category:
            raise RateCategoryNotFoundError("Category not found.")
        
        rate_customization = await self.customization_repo.get(rate_category.rate_customization_id, user_id)
        
        if not rate_customization:
            if await self.customization_repo.is_irs_customization(rate_category.rate_customization_id):
                rate_customization = await self.customization_repo.get(rate_category.rate_customization_id)
        
        if not rate_customization:
            raise RateCategoryNotFoundError("Category not found or not accessible to user.")
        
        return rate_category
    
    async def get_categories_by_customization(self, user_id: UUID, customization_id: UUID):
        rate_customization = await self.customization_repo.get(customization_id, user_id)
        
        if not rate_customization:
            if await self.customization_repo.is_irs_customization(customization_id):
                rate_customization = await self.customization_repo.get(customization_id)
        
        if not rate_customization:
            raise RateCustomizationNotFoundError("Customization not found or not accessible to user.")

        try:
            categories = await self.category_repo.get_by_customization_id(customization_id)
            return categories
        except Exception as e:
            raise RateCategoryPersistenceError("Unexpected error occurred while fetching categories") from e
    
    async def edit_category(self, user_id: UUID, category_id: UUID, data: EditRateCategoryDTO):
        rate_category = await self.get_category(user_id, category_id)
        
        if await self.customization_repo.is_irs_customization(rate_category.rate_customization_id):
            raise InvalidRateCategoryDataError("Cannot modify IRS standard rate categories")

        if data.name is not None:
            if not data.name.strip():
                raise InvalidRateCategoryDataError("Name cannot be empty")
            cleaned_name = data.name.strip()
            if cleaned_name != rate_category.name:
                existing = await self.category_repo.get_by_customization_and_name(
                    rate_category.rate_customization_id, 
                    cleaned_name
                )
                if existing:
                    raise DuplicateRateCategoryError("A rate category with this name already exists for this customization")
            rate_category.name = cleaned_name

        if data.cost_per_mile is not None:
            if data.cost_per_mile <= 0:
                raise InvalidRateCategoryDataError("Cost per mile must be a non-negative number")
            rate_category.cost_per_mile = data.cost_per_mile

        try:
            return await self.category_repo.save(rate_category)
        except Exception as e:
            raise RateCategoryPersistenceError("Unexpected error occurred while updating rate category") from e
    
    async def delete_category(self, user_id: UUID, category_id: UUID):
        rate_category = await self.get_category(user_id, category_id)
        
        if await self.customization_repo.is_irs_customization(rate_category.rate_customization_id):
            raise InvalidRateCategoryDataError("Cannot delete IRS standard rate categories")
            
        return await self.category_repo.delete(rate_category)
    

