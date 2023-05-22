from enum import Enum, auto

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

engine: AsyncEngine | None = None
sessionmaker: async_sessionmaker[AsyncSession] | None = None


class FieldValue(Enum):
    ANY = auto()
    NOT_NONE = auto()
