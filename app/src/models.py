import re

from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


class Building(Base):
    """Здание"""

    __tablename__ = 'buildings'

    id = Column(
        Integer,
        primary_key=True,
    )
    address = Column(
        String,
        unique=True,
        nullable=False,
    )
    location = Column(
        Geometry(geometry_type='POINT', srid=4326),
    )


class Organization(Base):
    """Организация"""

    __tablename__ = 'organizations'

    id = Column(
        Integer,
        primary_key=True,
    )
    title = Column(
        String,
        unique=True,
        nullable=False,
    )
    building_id = Column(
        Integer,
        ForeignKey('buildings.id'),
        nullable=False,
    )

    building = relationship('Building')


class Activity(Base):
    """Деятельность"""

    __tablename__ = 'activities'

    id = Column(
        Integer,
        primary_key=True,
    )
    title = Column(
        String,
        unique=True,
        nullable=False,
    )
    parent_id = Column(
        Integer,
        ForeignKey('activities.id'),
    )
    level = Column(
        Integer,
        nullable=False,
        default=0
    )

    parent = relationship('Activity', remote_side=[id], backref='children')

    MAX_LEVEL = 3

    async def set_level(self, session):
        if self.parent is not None:
            self.level = self.parent.level + 1
        elif self.parent_id is not None:
            parent = await session.get(Activity, self.parent_id)
            if parent is None:
                raise ValueError('Родитель не найден.')
            self.level = parent.level + 1
        else:
            self.level = 0
        if self.level > self.MAX_LEVEL:
            raise ValueError(f'Максимальная вложенность — {self.MAX_LEVEL}.')


class OrganizationActivity(Base):
    """Деятельность организации"""

    __tablename__ = 'organization_activities'

    id = Column(
        Integer,
        primary_key=True,
    )
    organization_id = Column(
        Integer,
        ForeignKey('organizations.id'),
        nullable=False,
    )
    activity_id = Column(
        Integer,
        ForeignKey('activities.id'),
        nullable=False,
    )

    organization = relationship('Organization')
    activity = relationship('Activity')


class PhoneNumber(Base):
    """Номер телефона"""

    __tablename__ = 'phone_numbers'

    id = Column(
        Integer,
        primary_key=True,
    )
    _number = Column(
        String,
        nullable=False,
    )
    organization_id = Column(
        Integer,
        ForeignKey('organizations.id'),
        nullable=False,
    )

    organization = relationship('Organization')

    NUMBER_FORMAT_1 = re.compile(r'^\d{1}-\d{3}-\d{3}$')
    NUMBER_FORMAT_2 = re.compile(r'^\d{1}-\d{3}-\d{3}-\d{2}-\d{2}$')

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not (
            self.NUMBER_FORMAT_1.match(value)
            or self.NUMBER_FORMAT_2.match(value)
        ):
            raise ValueError('Некорректный формат номера.')
        self._number = value
