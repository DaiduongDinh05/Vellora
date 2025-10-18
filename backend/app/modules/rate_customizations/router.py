from uuid import UUID
from fastapi import APIRouter, Depends, Response, status
from app.infra.db import AsyncSession
from app.modules.rate_customizations.service import RateCustomizationsService
from app.container import get_db
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.schemas import CreateRateCustomizationDTO, EditRateCustomizationDTO, RateCustomizationResponseDTO
from app.core.error_handler import error_handler



router = APIRouter(prefix="/rate_customizations") #will insert userid once implemented as this should live under users

def get_rate_customizations_service(db: AsyncSession = Depends(get_db)):
    return RateCustomizationsService(RateCustomizationRepo(db))

#will add user id once it is created
@router.post("/", response_model=RateCustomizationResponseDTO)
@error_handler
async def create_rate_customization(body: CreateRateCustomizationDTO, svc = Depends(get_rate_customizations_service)):
    rate_customization = await svc.create_rate_customization(body)
    return rate_customization

@router.get("/{customizations_id}", response_model=RateCustomizationResponseDTO)
@error_handler
async def get_customization(customization_id: UUID, svc = Depends(get_rate_customizations_service)):
    rate_customization = await svc.get_customization(customization_id)
    return rate_customization

@router.patch("/{customizations_id}", response_model=RateCustomizationResponseDTO)
@error_handler
async def edit_customization(body: EditRateCustomizationDTO, customization_id: UUID, svc = Depends(get_rate_customizations_service)):
    rate_customization = await svc.edit_customization(customization_id, body)
    return rate_customization

@router.delete("/{customizations_id}")
@error_handler
async def delete_customization(customization_id: UUID, svc = Depends(get_rate_customizations_service)):
    await svc.delete_customization(customization_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)