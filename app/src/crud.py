from src.schemas import LocationParams, PaginationParams, PaginatedResponse
from geoalchemy2.functions import ST_DWithin, ST_Point, ST_SetSRID
from src.models import Building, Organization, OrganizationActivity, Activity
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def get_organizations_by_building(
    id: int,
    pagination: PaginationParams,
    db: AsyncSession
):
    base_query = select(Organization).filter_by(building_id=id)
    count_query = (
        select(func.count())
        .select_from(Organization)
        .filter_by(building_id=id)
    )
    result_count = await db.execute(count_query)
    total = result_count.scalar_one()
    result_items = await db.execute(
        base_query
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
    )
    items = result_items.scalars().all()
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


async def get_organizations_by_activity(
    activity_id: int,
    pagination: PaginationParams,
    db: AsyncSession
):
    base_query = (
        select(Organization)
        .join(OrganizationActivity)
        .filter(OrganizationActivity.activity_id == activity_id)
    )
    count_query = (
        select(func.count())
        .select_from(Organization)
        .join(OrganizationActivity)
        .filter(OrganizationActivity.activity_id == activity_id)
    )
    result_count = await db.execute(count_query)
    total = result_count.scalar_one()
    result_items = await db.execute(
        base_query
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
    )
    items = result_items.scalars().all()
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


async def get_organizations_within_radius(
    pagination: PaginationParams,
    location: LocationParams,
    db: AsyncSession
):
    point = ST_SetSRID(ST_Point(location.lon, location.lat), 4326)
    base_query = (
        select(Organization)
        .join(Building)
        .filter(ST_DWithin(Building.location, point, location.radius))
    )
    count_query = (
        select(func.count())
        .select_from(Organization)
        .join(Building)
        .filter(ST_DWithin(Building.location, point, location.radius))
    )
    result_count = await db.execute(count_query)
    total = result_count.scalar_one()
    result_items = await db.execute(
        base_query
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
    )
    items = result_items.scalars().all()
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


async def get_buildings_within_radius(
    pagination: PaginationParams,
    location: LocationParams,
    db: AsyncSession
):
    point = ST_SetSRID(ST_Point(location.lon, location.lat), 4326)
    base_query = (
        select(Building)
        .filter(ST_DWithin(Building.location, point, location.radius))
    )
    count_query = (
        select(func.count())
        .select_from(Building)
        .filter(ST_DWithin(Building.location, point, location.radius))
    )
    result_count = await db.execute(count_query)
    total = result_count.scalar_one()
    result_items = await db.execute(
        base_query.offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
    )
    items = result_items.scalars().all()
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


async def get_organizations_by_activity_title(
    pagination: PaginationParams,
    title: str,
    db: AsyncSession
):
    base_query = (
        select(Organization)
        .join(OrganizationActivity)
        .join(Activity)
        .filter(Activity.title.ilike(f'%{title}%'))
    )
    count_query = (
        select(func.count())
        .select_from(Organization)
        .join(OrganizationActivity)
        .join(Activity)
        .filter(Activity.title.ilike(f'%{title}%'))
    )
    result_count = await db.execute(count_query)
    total = result_count.scalar_one()
    result_items = await db.execute(
        base_query
        .offset((pagination.page - 1) * pagination.size)
        .limit(pagination.size)
    )
    items = result_items.scalars().all()
    return PaginatedResponse(
        total=total,
        items=items,
        page=pagination.page,
        size=pagination.size
    )


async def get_organization_by_id(id: int, db: AsyncSession):
    result = await db.execute(select(Organization).filter_by(id=id))
    organization = result.scalars().first()
    if organization is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Организация не найдена.')
    return organization


async def get_building_by_id(id: int, db: AsyncSession):
    result = await db.execute(select(Building).filter_by(id=id))
    building = result.scalars().first()
    if building is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Организация не найдена.')
    return building


async def get_organization_by_title(title: str, db: AsyncSession):
    result = await db.execute(
        select(Organization)
        .filter(Organization.title.ilike(f'%{title}%'))
    )
    organization = result.scalars().first()
    if organization is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Организация не найдена.')
    return organization


async def get_activity_by_title(title: str, db: AsyncSession):
    result = await db.execute(
        select(Activity)
        .filter(Activity.title.ilike(f'%{title}%'))
    )
    activity = result.scalars().first()
    if activity is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Деятельность не найдена.')
    return activity
