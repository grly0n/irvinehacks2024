from typing_extensions import Annotated
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from database import Meal, meals_db

"""
All backend-to-frontend function calls are kept here
"""
app = FastAPI()

# Ensures that the meal IDs are unique
def ensure_no_duplicate(id: int, db: dict[int, Meal]) -> bool:
    for entry in db:
        if entry == id: return False
    return True


# Returns all meals logged in the database
@app.get("/meals", tags=["meals"])
async def get_meals():
    return {"data": meals_db}


# Adds a meal to the database (requires a unique ID)
@app.post("/meals", tags=["meals"])
async def add_meal(meal: Meal):
    if not ensure_no_duplicate(meal.id, meals_db):
        return {"data": "Meal not added, duplicate ID found"}
    meals_db[meal.id] = meal
    return {"data": "Meal added"}


# Updates a meal according to its ID
@app.put("/meals", tags=["meals"])
async def update_meals(id: int, newMeal: Meal):
    for meal in meals_db:
        if meal == id:
            meals_db[id] = newMeal
            return {"data": f"Meal with id {id} updated"}
    return {"data": f"Meal with id {id} not found"}


# Deletes a meal according to its ID
@app.delete("/meals", tags=["meals"])
async def remove_meal(id: int):
    for meal in meals_db:
        if meal == id:
            meals_db.pop(id)
            return {"data": f"Meal with id {id} removed"}
    return {"data": f"Meal with id {id} not found"}


# Placeholder main page
@app.get("/")
async def main():
    content = """
    <body>
        <h1>Welcome to Dining Hall Menu 2!</h1>
        <p>This is a placeholder for the home screen which will go here soon</p>
    </body>
"""
    return HTMLResponse(content)


@app.get("/home")
def home():
    return {"message": "This is the home page"}
