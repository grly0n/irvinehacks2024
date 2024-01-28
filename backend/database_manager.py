from scraper import dining_scraper
from pathlib import Path
import json
import time

# Structure of database: db[date: str][meal: str][station: str][food: list[str]]

# Returns a database from the loaded pseudo-JSON (txt) file
#def read_from_file(file : bytes) -> dict[str, dict[str, dict[str, list[str]]]]:
#    return json.dumps(file.decode())


def read_into_file(data: dict[str,  dict[str, dict[str, list[str]]]], file_name: str):
    '''Reads a database object into a text file as JSON data'''
    with open(file_name, 'w') as f:
        f.write(json.dumps(data))


def get_database(eatery_id: str, file_name: str):
    '''Scrapes the dining site corresponding with the ID, reads the database into a file, and returns the start time.'''
    output = dining_scraper.get_info(eatery_id)
    read_into_file(output[0], file_name)
    return output[1]


def manage_database(load: bool):
    '''Automatically updates databases every 7 days. Pass load as True to load manually.'''
    brandywine_start_time = time.time()
    p = Path().absolute() / 'frontend/src/components/pages'
    print(p.exists())

    # Load databases manually (only for the first time)
    if load:
        try:
            get_database("TheAnteatery", p / "anteatery_database.json")
            brandywine_start_time = get_database("BrandyWine", p / "brandywine_database.json")
        except:
            manage_database(load)


    # Main loop updating information every 7 days
    while True:
        print("Checking whether to update")
        if time.time() - brandywine_start_time >= 604800:
            print("Updating...")
            get_database("TheAnteatery", p / "anteatery_database.json")
            brandywine_start_time = get_database("BrandyWine", p / "brandywine_database.json")
            print("Database updated")
        else: 
            print("Not updating")
            time.sleep(604800)

if __name__ == "__main__":
    manage_database(False)

