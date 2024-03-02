from typing import Callable

from fastapi import FastAPI

from app.core.database import Database


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app():
        database = Database()
        database.create_database()

    return start_app
