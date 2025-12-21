from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routers.Healthy_Check import healthy_check_router
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_app():

    settings = get_settings()
    
    app.mongo_conn = AsyncIOMotorClient(settings.CONNECTION_URL)
    app.db_client = app.mongo_conn[settings.DATABASE_NAME]



@app.on_event("shutdown")
async def shutdown_app():
    app.mongo_conn.close()


app.include_router(healthy_check_router)