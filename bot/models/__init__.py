from gino import Gino

db = Gino()


async def bind_database(postgres_login: str):
    await db.set_bind(postgres_login)
