from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    full_name: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TripSearch(BaseModel):
    departure: str
    departureCity: str
    destination: str
    destinationCity: str
    departDate: str
