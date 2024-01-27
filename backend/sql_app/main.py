from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import session

from . import crud, models, schemas
from .database import SessionLocal, engine
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/locations/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: session = Depends(get_db)):
    db_location = crud.get_location(db, location.id)
    if db_location:
        raise HTTPException(status_code=400, detail="Location already registered")
    return crud.create_location(db=db, location=location)


@app.get("/locations/", response_model=list[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: session = Depends(get_db)):
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations


@app.get("/locations/{location_id}", response_model=schemas.Location)
def read_location(location_id: int, db: session = Depends(get_db)):
    db_location = crud.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@app.post("/locations/{location_id}/meals/", response_model=schemas.Meal)
def create_meal_for_location(
    location_id: int, meal: schemas.MealCreate, db: session = Depends(get_db)
):
    return crud.create_meal(db, meal=meal, location_id=location_id)


@app.get("/meals/", response_model=list[schemas.Meal])
def read_meals(skip: int = 0, limit: int = 100, db: session = Depends(get_db)):
    meals = crud.get_meals(db, skip=skip, limit=limit)
    return meals


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)