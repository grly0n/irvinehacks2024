"""
app.py

This one file is all you need to start off with your FastAPI server!
"""

from typing_extensions import Annotated
from pydantic import BaseModel
import datetime


import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse



app = FastAPI()


class Meal(BaseModel):
    id: int
    location: str
    time: str
    type: str


meals_db = dict()


def ensure_no_duplicate(id: int, db: dict[int, Meal]) -> bool:
    for entry in db:
        if entry == id: return False
    return True


@app.get("/meals", tags=["meals"])
async def get_meals():
    return {"data": meals_db}


@app.post("/meals", tags=["meals"])
async def add_meal(meal: Meal):
    if not ensure_no_duplicate(meal.id, meals_db):
        return {"data": "Meal not added, duplicate ID found"}
    meals_db[meal.id] = meal
    return {"data": "Meal added"}


@app.put("/meals", tags=["meals"])
async def update_meals(id: int, newMeal: Meal):
    for meal in meals_db:
        if meal == id:
            meals_db[id] = newMeal
            return {"data": f"Meal with id {id} updated"}
    return {"data": f"Meal with id {id} not found"}


@app.delete("/meals", tags=["meals"])
async def remove_meal(id: int):
    for meal in meals_db:
        if meal == id:
            meals_db.pop(id)
            return {"data": f"Meal with id {id} removed"}
    return {"data": f"Meal with id {id} not found"}


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


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)
