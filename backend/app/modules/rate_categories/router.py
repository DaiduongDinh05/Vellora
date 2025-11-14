from uuid import UUID
from fastapi import APIRouter, Depends, Response, status
from app.infra.db import AsyncSession
from app.modules.rate_categories.service import RateCategoriesService
from app.container import get_db
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_categories.schemas import CreateRateCategoryDTO, EditRateCategoryDTO, RateCategoryResponseDTO
from app.core.error_handler import error_handler
from app.modules.rate_customizations.repository import RateCustomizationRepo



router = APIRouter(prefix="/rate_customizations/{customization_id}/rate_categories", tags=["Rate Categories"]) #will insert userid once implemented as this should live under users

def get_rate_category_service(db: AsyncSession = Depends(get_db)):
    return RateCategoriesService(RateCategoryRepo(db), RateCustomizationRepo(db))

@router.post("/", response_model=RateCategoryResponseDTO)
@error_handler
async def create_rate_category(body: CreateRateCategoryDTO, customization_id: UUID, svc = Depends(get_rate_category_service)):
    rate_category = await svc.create_rate_category(customization_id, body)
    return rate_category

@router.get("/", response_model=list[RateCategoryResponseDTO])
@error_handler
async def get_categories_by_customization(customization_id: UUID, svc = Depends(get_rate_category_service)):
    categories_by_customization = await svc.get_categories_by_customization(customization_id)
    return categories_by_customization

@router.get("/{category_id}", response_model=RateCategoryResponseDTO)
@error_handler
async def get_category(category_id: UUID, svc = Depends(get_rate_category_service)):
    rate_category = await svc.get_category(category_id)
    return rate_category


@router.patch("/{category_id}", response_model=RateCategoryResponseDTO)
@error_handler
async def edit_category(body: EditRateCategoryDTO, category_id: UUID, svc = Depends(get_rate_category_service)):
    rate_category = await svc.edit_category(category_id, body)
    return rate_category

@router.delete("/{category_id}")
@error_handler
async def delete_category(category_id: UUID, svc = Depends(get_rate_category_service)):
    await svc.delete_category(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)