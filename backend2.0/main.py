import subprocess
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

class TripSearch(BaseModel):
    departure: str
    destination: str
    departDate: str
    returnDate: str


app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/search')
async def search_trips(trip: TripSearch):
    try:
        result = subprocess.run(
            ["python", "scraping.py",
             trip.departure,
             trip.destination,
             trip.departDate,
             trip.returnDate],
            capture_output=True,
            text=True,
            cwd="/home/esolzey/repos/thesis/backend2.0"
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
