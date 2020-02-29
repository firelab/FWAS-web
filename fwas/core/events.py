from typing import Callable

from fastapi import FastAPI
from loguru import logger

from fwas.database import database


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        if not database.is_connected:
            await database.connect()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        if database.is_connected:
            await database.disconnect()

    return stop_app
