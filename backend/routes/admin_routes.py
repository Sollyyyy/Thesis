from fastapi import APIRouter, Depends, HTTPException
from auth import require_admin
from database import get_all_users, get_user, delete_user, get_search_history

router = APIRouter(prefix="/api/admin")


@router.get('/users')
async def admin_get_users(admin: dict = Depends(require_admin)):
    return get_all_users()


@router.delete('/users/{username}')
async def admin_delete_user(username: str, admin: dict = Depends(require_admin)):
    if username == admin["username"]:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    target = get_user(username)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(username)
    return {"message": f"User '{username}' deleted"}


@router.get('/history/{username}')
async def admin_get_history(username: str, admin: dict = Depends(require_admin)):
    return get_search_history(username)
