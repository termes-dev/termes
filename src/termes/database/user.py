from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..errors import ItemNotFoundError
from ..models import User


async def get_user(
        user_id: int,
        database_session: AsyncSession,
        *,
        include_profile: bool = False,
        include_credentials: bool = False,
        include_sessions: bool = False
) -> User:
    statement = select(User).where(User.id == user_id)
    if include_profile:
        statement.options(selectinload(User.profile))
    if include_credentials:
        statement.options(selectinload(User.credentials))
    if include_sessions:
        statement.options(selectinload(User.sessions))

    user = (await database_session.execute(statement)).scalar()

    if user is None:
        raise ItemNotFoundError()

    return user
