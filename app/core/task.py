from typing import Callable

from core.database import Database
from fastapi import FastAPI


def create_start_handler(app: FastAPI) -> Callable:
    async def start_app():
        database = Database()
        database.create_database()

    return start_app
