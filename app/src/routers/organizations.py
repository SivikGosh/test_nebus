from fastapi import APIRouter, Depends, Query
from src.dependencies import get_async_db
from src.schemas import (
    OrganizationSchema,
    LocationParams,
    PaginatedResponse,
    PaginationParams
)
from src import crud
from src.api_key import verify_secret_key
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    '/by-building/{id}',
    response_model=PaginatedResponse[OrganizationSchema],
    dependencies=(Depends(verify_secret_key),)
)
async def get_organizations_by_building(
    id: int,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    """Список организаций в здании по его ID."""
    return await crud.get_organizations_by_building(id, pagination, db)


@router.get(
    '/by-activity/{id}',
    response_model=PaginatedResponse[OrganizationSchema],
    dependencies=(Depends(verify_secret_key),)
)
async def get_organizations_by_activity(
    id: int,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    """Список организаций по ID деятельности."""
    return await crud.get_organizations_by_activity(id, pagination, db)


@router.get(
    '/radius',
    response_model=PaginatedResponse[OrganizationSchema],
    dependencies=(Depends(verify_secret_key),)
)
async def get_organizations_within_radius(
    pagination: PaginationParams = Depends(),
    location: LocationParams = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    """Список организаций в выбранном радиусе."""
    return await crud.get_organizations_within_radius(pagination, location, db)


@router.get(
    '/search_activity',
    response_model=PaginatedResponse[OrganizationSchema],
    dependencies=(Depends(verify_secret_key),)
)
async def get_organizations_by_activity_title(
    pagination: PaginationParams = Depends(),
    title: str = Query(),
    db: AsyncSession = Depends(get_async_db)
):
    """Список организаций по названию деятельности."""
    return await (
        crud.get_organizations_by_activity_title(pagination, title, db)
    )


@router.get(
    '/{id}',
    response_model=OrganizationSchema,
    dependencies=(Depends(verify_secret_key),)
)
async def get_organization_by_id(
    id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Получить организацию по ID."""
    return await crud.get_organization_by_id(id, db)


@router.get(
    '/',
    response_model=OrganizationSchema,
    dependencies=(Depends(verify_secret_key),)
)
async def get_organization_by_title(
    title: str,
    db: AsyncSession = Depends(get_async_db)
):
    """Получить организацию по названию."""
    return await crud.get_organization_by_title(title, db)
