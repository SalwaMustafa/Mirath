from fastapi import APIRouter
import os
from helpers.config import settings, get_settings

healthy_check_router = APIRouter()

@healthy_check_router.get("/health-check")
async def welcome():

    app_settings: settings = get_settings()
    app_name = app_settings.APP_NAME

    return {
        "app_name": app_name,
    }