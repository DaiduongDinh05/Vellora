import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from app.modules.rate_customizations.service import RateCustomizationsService
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.schemas import CreateRateCustomizationDTO, EditRateCustomizationDTO
from app.modules.rate_customizations.models import RateCustomization
from app.modules.rate_customizations.exceptions import (
    InvalidRateCustomizationDataError,
    RateCustomizationPersistenceError,
    RateCustomizationNotFoundError
)


class TestRateCustomizationsServiceCreate:

    @pytest.fixture
    def mock_repo(self):
        return AsyncMock(spec=RateCustomizationRepo)

    @pytest.mark.asyncio
    async def test_create_customization_success(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        dto = CreateRateCustomizationDTO(
            name="Business Rates 2024",
            description="Standard business mileage rates",
            year=2024
        )
        mock_customization = MagicMock(spec=RateCustomization)
        mock_repo.save.return_value = mock_customization

        with patch('app.modules.rate_customizations.service.RateCustomization', return_value=mock_customization):
            result = await service.create_rate_customization(dto)

        assert result == mock_customization
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_customization_empty_name(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        dto = CreateRateCustomizationDTO(name="   ", description="Test", year=2024)

        with pytest.raises(InvalidRateCustomizationDataError) as exc_info:
            await service.create_rate_customization(dto)
        assert "Name is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_customization_missing_year(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        dto = CreateRateCustomizationDTO(name="Test", description="Test", year=0)

        with pytest.raises(InvalidRateCustomizationDataError) as exc_info:
            await service.create_rate_customization(dto)
        assert "Year is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_customization_persistence_error(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        dto = CreateRateCustomizationDTO(
            name="Business Rates 2024",
            description="Test",
            year=2024
        )
        mock_repo.save.side_effect = Exception("Database error")

        with pytest.raises(RateCustomizationPersistenceError) as exc_info:
            await service.create_rate_customization(dto)
        assert "Unexpected error occured while saving customziation" in str(exc_info.value)


class TestRateCustomizationsServiceGet:

    @pytest.fixture
    def mock_repo(self):
        return AsyncMock(spec=RateCustomizationRepo)

    @pytest.mark.asyncio
    async def test_get_customization_success(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        mock_customization = MagicMock(spec=RateCustomization)
        mock_repo.get.return_value = mock_customization

        result = await service.get_customization(customization_id)

        assert result == mock_customization
        mock_repo.get.assert_called_once_with(customization_id)

    @pytest.mark.asyncio
    async def test_get_customization_not_found(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        mock_repo.get.return_value = None

        with pytest.raises(RateCustomizationNotFoundError) as exc_info:
            await service.get_customization(customization_id)
        assert "Customization not found" in str(exc_info.value)


class TestRateCustomizationsServiceEdit:

    @pytest.fixture
    def mock_repo(self):
        return AsyncMock(spec=RateCustomizationRepo)

    @pytest.fixture
    def mock_customization(self):
        customization = MagicMock(spec=RateCustomization)
        customization.id = uuid4()
        customization.name = "Original Name"
        customization.description = "Original Description"
        customization.year = 2024
        return customization

    @pytest.mark.asyncio
    async def test_edit_customization_success(self, mock_repo, mock_customization):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        dto = EditRateCustomizationDTO(
            name="Updated Name",
            description="Updated Description",
            year=2025
        )
        mock_repo.get.return_value = mock_customization
        mock_repo.save.return_value = mock_customization

        result = await service.edit_customization(customization_id, dto)

        assert result == mock_customization
        assert mock_customization.name == "Updated Name"
        assert mock_customization.description == "Updated Description"
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_edit_customization_partial_update(self, mock_repo, mock_customization):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        dto = EditRateCustomizationDTO(name="Updated Name")
        mock_repo.get.return_value = mock_customization
        mock_repo.save.return_value = mock_customization

        result = await service.edit_customization(customization_id, dto)

        assert result == mock_customization
        assert mock_customization.name == "Updated Name"
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_edit_customization_not_found(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        dto = EditRateCustomizationDTO(name="Updated Name")
        mock_repo.get.return_value = None

        with pytest.raises(RateCustomizationNotFoundError):
            await service.edit_customization(customization_id, dto)

    @pytest.mark.asyncio
    async def test_edit_customization_empty_name(self, mock_repo, mock_customization):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        dto = EditRateCustomizationDTO(name="   ")
        mock_repo.get.return_value = mock_customization

        with pytest.raises(InvalidRateCustomizationDataError) as exc_info:
            await service.edit_customization(customization_id, dto)
        assert "name cannot be empty" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_edit_customization_invalid_year(self, mock_repo, mock_customization):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        dto = EditRateCustomizationDTO(year=0)
        mock_repo.get.return_value = mock_customization

        with pytest.raises(InvalidRateCustomizationDataError) as exc_info:
            await service.edit_customization(customization_id, dto)
        assert "Year is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_edit_customization_strips_name(self, mock_repo, mock_customization):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        dto = EditRateCustomizationDTO(name="  Updated Name  ")
        mock_repo.get.return_value = mock_customization
        mock_repo.save.return_value = mock_customization

        result = await service.edit_customization(customization_id, dto)

        assert mock_customization.name == "Updated Name"


class TestRateCustomizationsServiceDelete:

    @pytest.fixture
    def mock_repo(self):
        return AsyncMock(spec=RateCustomizationRepo)

    @pytest.mark.asyncio
    async def test_delete_customization_success(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        mock_customization = MagicMock(spec=RateCustomization)
        mock_repo.get.return_value = mock_customization
        mock_repo.delete.return_value = None

        result = await service.delete_customization(customization_id)

        mock_repo.delete.assert_called_once_with(mock_customization)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_customization_not_found(self, mock_repo):
        service = RateCustomizationsService(mock_repo)
        customization_id = uuid4()
        mock_repo.get.return_value = None

        with pytest.raises(RateCustomizationNotFoundError):
            await service.delete_customization(customization_id)
