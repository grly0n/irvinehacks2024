import uvicorn
from api_functions import app

import json
from scraper import dining_scraper
import time
from pathlib import Path

# Structure of database: db[(month, day)][meal][station][food]

# Returns a database from the loaded pseudo-JSON (txt) file
def read_from_file(file : bytes) -> dict[str, dict[str, dict[str, list[str]]]]:
    return json.dumps(file.decode())


def read_into_file(data: dict[str,  dict[str, dict[str, list[str]]]], file_name: str):
    with open(file_name, 'w') as f:
        f.write(json.dumps(data))


def get_database(eatery_id: str, file_name: str):
    output = dining_scraper.get_info(eatery_id)
    read_into_file(output[0], file_name)
    return output[1]


if __name__ == "__main__":
    LOAD = True
    anteatery_start_time = 0 
    brandywine_start_time = 0
    p = Path().absolute() / 'backend/database'

    if LOAD:
        anteatery_start_time = get_database("TheAnteatery", p / "anteatery_database.txt")
        brandywine_start_time = get_database("BrandyWine", p / "brandywine_database.txt")

    uvicorn.run("main:app", port=5000, reload=True)

    while True:
        if time.time() - brandywine_start_time > 604800:
            anteatery_start_time = get_database("TheAnteatery", "database/anteatery_database.txt")
            brandywine_start_time = get_database("BrandyWine", "database/brandywine_database.txt")

