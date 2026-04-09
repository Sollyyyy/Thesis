import subprocess
import sys
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import json
import jwt
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from database import init_db, get_user, create_user, get_all_users, delete_user

ph = PasswordHasher()

SECRET_KEY = 'cf1c7f5f8500ce42346b06f2abb815e18409f787e1e69c3209816e7daa241792'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

init_db()


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@app.post('/api/register')
async def register(user: UserRegister):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = ph.hash(user.password)
    create_user(user.username, user.email, user.full_name, hashed_password)
    return {"message": "User registered successfully"}


@app.post('/api/login')
async def login(user: UserLogin):
    db_user = get_user(user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    try:
        ph.verify(db_user["hashed_password"], user.password)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": user.username, "role": db_user.get("role", "user")})
    return {"access_token": token, "token_type": "bearer"}


@app.get('/api/profile')
async def profile(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user.get("role", "user"),
    }


# Admin endpoints
@app.get('/api/admin/users')
async def admin_get_users(admin: dict = Depends(require_admin)):
    return get_all_users()


@app.delete('/api/admin/users/{username}')
async def admin_delete_user(username: str, admin: dict = Depends(require_admin)):
    if username == admin["username"]:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    target = get_user(username)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(username)
    return {"message": f"User '{username}' deleted"}


def run_script(script, args):
    try:
        result = subprocess.run(
            [sys.executable, script] + args,
            capture_output=True,
            text=True,
            cwd="/home/esolzey/repos/thesis/backend2.0"
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post('/api/search')
async def search_all(trip: TripSearch):
    flight = run_script("scraping.py", [
        trip.departure, trip.destination, trip.departDate, trip.returnDate
    ])
    train = run_script("train_scraping.py", [
        trip.departureCity, trip.destinationCity, trip.departDate
    ])
    bus = run_script("bus_scraping.py", [
        trip.departureCity, trip.destinationCity, trip.departDate
    ])
    return {"flight": flight, "bus": bus, "train": train}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
