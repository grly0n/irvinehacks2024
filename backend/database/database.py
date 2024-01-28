import json
import scraper

# Structure of database: db[(month, day)][meal][station][food]

# Returns a database from the loaded pseudo-JSON (txt) file
def read_from_file(file : bytes) -> dict[(int, int), dict[str, dict[str, list[str]]]]:
    return json.dumps(file.decode())

