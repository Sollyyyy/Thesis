from fastapi import APIRouter, Depends
from auth import get_current_user
from database import get_search_history

router = APIRouter(prefix="/api")


@router.get('/profile')
async def profile(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user.get("role", "user"),
    }


@router.get('/history')
async def get_history(user: dict = Depends(get_current_user)):
    return get_search_history(user["username"])
