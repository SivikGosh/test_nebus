from fastapi import APIRouter, Depends
from src.dependencies import get_async_db
from src.schemas import (
    BuildingSchema,
    LocationParams,
    PaginatedResponse,
    PaginationParams
)
from src import crud
from src.api_key import verify_secret_key
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    '/radius',
    response_model=PaginatedResponse[BuildingSchema],
    dependencies=(Depends(verify_secret_key),)
)
async def get_buildings_within_radius(
    pagination: PaginationParams = Depends(),
    location: LocationParams = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    """Список зданий в указанном радиусе."""
    return await crud.get_buildings_within_radius(pagination, location, db)


@router.get(
    '/{id}',
    response_model=BuildingSchema,
    dependencies=(Depends(verify_secret_key),)
)
async def get_organization_by_id(
    id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Получить организацию по ID."""
    return await crud.get_building_by_id(id, db)
