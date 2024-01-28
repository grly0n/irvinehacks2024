from pydantic import BaseModel
import sqlite3

class Meal(BaseModel):
    id: int
    location: str
    date: str
    type: str


meals_db = dict()

try:
    sqliteConnection = sqlite3.connect('sql_app.db')

except sqlite3.Error as error:
    print(f'Error ocurred - {error}')

finally:
    if sqliteConnection:
        sqliteConnection.close()   
        print('SQLite connection closed')
