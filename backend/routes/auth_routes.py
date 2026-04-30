from fastapi import APIRouter, HTTPException
from models import UserRegister, UserLogin
from auth import ph, create_access_token
from database import get_user, create_user

router = APIRouter(prefix="/api")


@router.post('/register')
async def register(user: UserRegister):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = ph.hash(user.password)
    create_user(user.username, user.email, user.full_name, hashed_password)
    return {"message": "User registered successfully"}


@router.post('/login')
async def login(user: UserLogin):
    db_user = get_user(user.username)
    if not db_user:
        raise HTTPException(status_code=401,
                            detail="Invalid username or password")
    try:
        ph.verify(db_user["hashed_password"], user.password)
    except Exception:
        raise HTTPException(status_code=401,
                            detail="Invalid username or password")
    token = create_access_token({"sub": user.username,
                                 "role": db_user.get("role", "user")})
    return {"access_token": token, "token_type": "bearer"}
