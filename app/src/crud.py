from sqlalchemy.orm import Session
from src.schemas import LocationParams, PaginationParams, PaginatedResponse
from geoalchemy2.functions import ST_DWithin, ST_Point, ST_SetSRID
from src.models import Building, Organization, OrganizationActivity, Activity
from fastapi import HTTPException
from http import HTTPStatus


def get_organizations_by_building(
    id: int,
    pagination: PaginationParams,
    db: Session
):
    organizations = (
        db.query(Organization)
        .filter_by(building_id=id)
    )
    total = organizations.count()
    items = (
        organizations
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
        .all()
    )
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


def get_organizations_by_activity(
    activity_id: int,
    pagination: PaginationParams,
    db: Session
):
    organizations = (
        db.query(Organization)
        .join(OrganizationActivity)
        .filter(OrganizationActivity.activity_id == activity_id)
    )
    total = organizations.count()
    items = (
        organizations
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
        .all()
    )
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


def get_organizations_within_radius(
    pagination: PaginationParams,
    location: LocationParams,
    db: Session
):
    point = ST_SetSRID(ST_Point(location.lon, location.lat), 4326)
    organizations = (
        db.query(Organization)
        .join(Building)
        .filter(ST_DWithin(Building.location, point, location.radius))
    )
    total = organizations.count()
    items = (
        organizations
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
        .all()
    )
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


def get_buildings_within_radius(
    pagination: PaginationParams,
    location: LocationParams,
    db: Session
):
    point = ST_SetSRID(ST_Point(location.lon, location.lat), 4326)
    buildings = (
        db.query(Building)
        .filter(ST_DWithin(Building.location, point, location.radius))
    )
    total = buildings.count()
    items = (
        buildings
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
        .all()
    )
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


def get_organizations_by_activity_title(
    pagination: PaginationParams,
    title: str,
    db: Session
):
    organizations = (
        db.query(Organization)
        .join(OrganizationActivity)
        .join(Activity)
        .filter(Activity.title.ilike(f'%{title}%'))
    )
    total = organizations.count()
    items = (
        organizations
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
        .all()
    )
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


def get_organization_by_id(id: int, db: Session):
    organization = db.query(Organization).filter_by(id=id).first()
    if organization is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Организация не найдена.')
    return organization


def get_organization_by_title(title: str, db: Session):
    organization = (
        db.query(Organization)
        .filter(Organization.title.ilike(f'%{title}%'))
        .first()
    )
    if organization is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Организация не найдена.')
    return organization
