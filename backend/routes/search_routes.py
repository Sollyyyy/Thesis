import os
import json
import asyncio
from fastapi import APIRouter, Depends
from models import TripSearch
from auth import get_current_user_optional
from database import save_search
from services.search_service import run_script

router = APIRouter(prefix="/api")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                       'airports.json'), 'r') as f:
    AIRPORTS = json.load(f)


@router.get('/airports')
async def get_available_airports():
    return AIRPORTS


@router.post('/search')
async def search_all(trip: TripSearch,
                     user: dict = Depends(get_current_user_optional)):
    if user:
        save_search(user["username"], trip.departureCity, trip.destinationCity,
                    trip.departDate)

    flight, train, bus = await asyncio.gather(
        run_script("scraping.py", [
            trip.departure, trip.destination, trip.departDate
        ]),
        run_script("train_scraping.py", [
            trip.departureCity, trip.destinationCity, trip.departDate
        ]),
        run_script("bus_scraping.py", [
            trip.departureCity, trip.destinationCity, trip.departDate
        ])
    )

    return {"flight": flight, "bus": bus, "train": train}
