from sqlalchemy.orm import session

from . import models, schemas

def get_location(db: session, location_id: int):
    return db.query(models.LocationsAndDates).filter(models.LocationsAndDates.id == location_id).first()


def get_locations(db: session, skip: int = 0, limit: int = 100):
    return db.query(models.LocationsAndDates).offset(skip).limit(limit).all()


def create_location(db: session, location: schemas.LocationCreate):
    db_location = models.LocationsAndDates(name = location.name)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_meals(db: session, skip: int = 0, limit: int = 100):
    return db.query(models.Meals).offset(skip).limit(100).all()


def create_meal(db: session, meal: schemas.MealCreate, location_id: int):
    db_meal = models.Meals(**meal.model_dump(), location_id=location_id)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal