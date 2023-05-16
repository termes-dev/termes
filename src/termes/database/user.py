from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .. import utils
from ..errors import ItemNotFoundError
from ..models import User, UserCredentials


async def get_user(
        database_session: AsyncSession,
        user_id: int,
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


async def delete_user(database_session: AsyncSession, user_id: int, delete_from_database: bool = False):
    if delete_from_database:
        statement = delete(User).where(User.id == user_id)
    else:
        statement = update(User).where(User.id == user_id).values(deleted=True)

    await database_session.execute(statement)


async def check_credentials(database_session: AsyncSession, email: str, password: str | None = None) -> bool:
    statement = select(func.count()).select_from(UserCredentials).where(UserCredentials.email == email)

    if password is not None:
        statement.where(UserCredentials.hashed_password == utils.sha256(password))

    count = (await database_session.execute(statement)).scalar()

    return count > 0
