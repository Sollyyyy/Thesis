import os
import json
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
async def get_airports():
    return AIRPORTS


@router.post('/search')
async def search_all(trip: TripSearch,
                     user: dict = Depends(get_current_user_optional)):
    if user:
        save_search(user["username"], trip.departureCity, trip.destinationCity,
                    trip.departDate, trip.returnDate)

    flight = run_script("scraping.py", [
        trip.departure, trip.destination, trip.departDate, trip.returnDate
    ])
    train = run_script("train_scraping.py", [
        trip.departureCity, trip.destinationCity, trip.departDate
    ])
    bus = run_script("bus_scraping.py", [
        trip.departureCity, trip.destinationCity, trip.departDate
    ])

    if trip.returnDate:
        train_return = run_script("train_scraping.py", [
            trip.destinationCity, trip.departureCity, trip.returnDate
        ])
        bus_return = run_script("bus_scraping.py", [
            trip.destinationCity, trip.departureCity, trip.returnDate
        ])
    else:
        train_return = None
        bus_return = None

    return {
        "flight": flight,
        "bus": bus,
        "train": train,
        "bus_return": bus_return,
        "train_return": train_return
    }
