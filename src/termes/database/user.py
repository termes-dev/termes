from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from termes.errors import ItemNotFoundError
from termes.models import User, UserProfile


async def get_user(
        database_session: AsyncSession,
        user_id: int,
        *,
        include_profile: bool = False,
        include_credentials: bool = False,
        include_sessions: bool = False
) -> User:
    options = []
    if include_profile:
        options.append(selectinload(User.profile))
    if include_credentials:
        options.append(selectinload(User.credentials))
    if include_sessions:
        options.append(selectinload(User.sessions))

    user = await database_session.get(User, user_id, options=options)

    if user is None:
        raise ItemNotFoundError()

    return user


async def find_user_by_username(
        database_session: AsyncSession,
        username: str,
        *,
        include_profile: bool = False,
        include_credentials: bool = False,
        include_sessions: bool = False
) -> User:
    user_id = (
        await database_session.execute(
            select(UserProfile.user_id).where(UserProfile.username == username)
        )
    ).scalar()

    if user_id is None:
        raise ItemNotFoundError()

    return await get_user(
        database_session,
        user_id,
        include_profile=include_profile,
        include_credentials=include_credentials,
        include_sessions=include_sessions
    )


async def check_username(database_session: AsyncSession, username: str) -> bool:
    stmt = select(func.count()).select_from(UserProfile).where(UserProfile.username == username)

    count = (await database_session.execute(stmt)).scalar()

    return count > 0


async def add_user(database_session: AsyncSession, user: User):
    database_session.add(user)
    await database_session.flush()


async def delete_user(database_session: AsyncSession, user_id: int):
    await database_session.delete(User(id=user_id))
