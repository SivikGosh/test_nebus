from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.schemas import (
    OrganizationSchema,
    LocationParams,
    PaginatedResponse,
    PaginationParams
)
from src import crud

router = APIRouter()


@router.get(
    '/by-building/{id}',
    response_model=PaginatedResponse[OrganizationSchema]
)
def get_organizations_by_building(
    id: int,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """Список организаций в здании по его ID."""
    return crud.get_organizations_by_building(id, pagination, db)


@router.get(
    '/by-activity/{id}',
    response_model=PaginatedResponse[OrganizationSchema]
)
def get_organizations_by_activity(
    id: int,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """Список организаций по ID деятельности."""
    return crud.get_organizations_by_activity(id, pagination, db)


@router.get('/radius', response_model=PaginatedResponse[OrganizationSchema])
def get_organizations_within_radius(
    pagination: PaginationParams = Depends(),
    location: LocationParams = Depends(),
    db: Session = Depends(get_db)
):
    """Список организаций в выбранном радиусе."""
    return crud.get_organizations_within_radius(pagination, location, db)


@router.get(
    '/search_activity',
    response_model=PaginatedResponse[OrganizationSchema]
)
def get_organizations_by_activity_title(
    pagination: PaginationParams = Depends(),
    title: str = Query(),
    db: Session = Depends(get_db)
):
    """Список организаций по названию деятельности."""
    return crud.get_organizations_by_activity_title(pagination, title, db)


@router.get('/{id}', response_model=OrganizationSchema)
def get_organization_by_id(id: int, db: Session = Depends(get_db)):
    """Получить организацию по ID."""
    return crud.get_organization_by_id(id, db)


@router.get('/', response_model=OrganizationSchema)
def get_organization_by_title(title: str, db: Session = Depends(get_db)):
    """Получить организацию по названию."""
    return crud.get_organization_by_title(title, db)
