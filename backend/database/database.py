import json

meals_db = dict() # Structure: meals_db[days_ahead][location][meal][station][food]

# Returns a database from the loaded pseudo-JSON (txt) file
def read_from_file(file : bytes) -> dict[(int, int), dict[str, dict[str, dict[str, list[str]]]]]:
    return json.dumps(file.decode())