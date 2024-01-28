from fastapi import FastAPI, File
from fastapi.responses import HTMLResponse
import database.database as db

from typing import Annotated

"""
All backend-to-frontend function calls are kept here
"""
app = FastAPI()
brandy_meals_db = dict()
anteat_meals_db = dict()

# Placeholder main page
@app.get("/")
async def main():
    content = """
    <body>
        <h1>Welcome to BrandyEatery!</h1>
        <p>Please upload database files</p>
        <form action="/files/" enctype="multipart/form-data" method="post">
        <input name="files" type = "file" multiple>
        <input type="submit">
        </form>
    </body>
"""
    return HTMLResponse(content)

# Returns all meals logged in the database
@app.get("/meals", tags=["meals"])
async def get_meals():
    return {"anteatery_db" : anteat_meals_db, "brandywine_db" : brandy_meals_db}


# Load databases from a text file
@app.post("/files/")
async def load_from_database(files: Annotated[list[bytes], File(description="Multiple files as bytes")]):
    brandy_meals_db = db.read_from_file(files[1])
    anteat_meals_db = db.read_from_file(files[0])
    return {"anteatery_db" : anteat_meals_db, "brandywine_db" : brandy_meals_db}