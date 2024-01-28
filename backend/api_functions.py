from fastapi import FastAPI, File, File
from fastapi.responses import HTMLResponse
import database.database as db

from typing import Annotated

"""
All backend-to-frontend function calls are kept here
"""
app = FastAPI()
db.meals_db = dict()

# Placeholder main page
@app.get("/")
async def main():
    content = """
    <body>
        <h1>Welcome to BrandyEatery!</h1>
        <p>Please upload database file</p>
        <form action="/load-from-database/" enctype="multipart/form-data" method="post">
        <input name="file" type = "file">
        <input type="submit">
        </form>
    </body>
"""
    return HTMLResponse(content)

# Returns all meals logged in the database
@app.get("/meals", tags=["meals"])
async def get_meals():
    return {"data": db.meals_db}

# Load database from a text file
@app.post("/load-from-database/", tags=["database"])
async def load_from_database(file: Annotated[bytes, File()]):
    db.meals_db = db.read_from_file(file)
    return {"message" : "Database loaded", "database" : db.meals_db}