from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class LocationsAndDates(Base):
    __tablename__ = "locationsAndDates"

    id = Column(Integer, primary_key=True)
    location = Column(String)
    date = Column(String)
    meal = Column(String)

    meals = relationship("Meals", back_populates="anteatery")
   

class Meals(Base):
    __tablename__ = "Meals"

    id = Column(Integer, primary_key=True)
    food = Column(String)
    location_id = Column(Integer, ForeignKey(LocationsAndDates.id))

    anteatery = relationship("LocationsAndDates", back_populates="meals")
