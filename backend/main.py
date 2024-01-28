import uvicorn
from api_functions import app


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)