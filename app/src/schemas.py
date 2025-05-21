from pydantic import BaseModel, Field
from fastapi import Query
from typing import List, Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar('T')


class PaginatedResponse(GenericModel, Generic[T]):
    total: int
    page: int
    items: List[T]


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=5, ge=1, le=100)


class BuildingSchema(BaseModel):
    id: int
    address: str

    class Config:
        from_attributes = True


class OrganizationSchema(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class LocationParams(BaseModel):
    lat: float = Query()
    lon: float = Query()
    radius: int = Query()
