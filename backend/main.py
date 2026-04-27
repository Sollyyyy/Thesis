import uvicorn
from fastapi import FastAPI
from database import init_db
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.search_routes import router as search_router
from routes.admin_routes import router as admin_router

init_db()

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(search_router)
app.include_router(admin_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
