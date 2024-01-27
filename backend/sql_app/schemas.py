from pydantic import BaseModel

class MealBase(BaseModel):
    name: str

class MealCreate(MealBase):
    pass

class Meal(MealBase):
    id: int
    location_id: int

    class Config:
        from_attributes = True


class LocationBase(BaseModel):
    name: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    meals: list[Meal] = []

    class Config:
        from_attributes = True