from pathlib import Path
import json

p = Path().absolute() / 'backend/database/anteatery_database.txt'
print(p.exists())

test = {"foo" : "bar"}

with open(p, 'w') as f:
    f.write(json.dumps(test))