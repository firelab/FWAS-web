from fwas.database import database


async def get_db():
    yield database


async def get_current_user():
    yield None
