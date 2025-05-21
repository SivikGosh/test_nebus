from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.schemas import (
    BuildingSchema,
    LocationParams,
    PaginatedResponse,
    PaginationParams
)
from src import crud

router = APIRouter()


@router.get('/radius', response_model=PaginatedResponse[BuildingSchema])
def get_buildings_within_radius(
    pagination: PaginationParams = Depends(),
    location: LocationParams = Depends(),
    db: Session = Depends(get_db)
):
    """Список зданий в указанном радиусе."""
    return crud.get_buildings_within_radius(pagination, location, db)
