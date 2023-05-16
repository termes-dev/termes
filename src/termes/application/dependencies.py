from sqlalchemy.ext.asyncio import AsyncSession

from .. import database


async def get_database_session() -> AsyncSession:
    session = database.sessionmaker()
    try:
        yield session
    finally:
        await session.close()