import secrets
from datetime import timedelta, datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .. import utils, schemas, models
from ..errors import ItemNotFoundError


async def get_user(
        database_session: AsyncSession,
        user_id: int,
        *,
        include_profile: bool = False,
        include_credentials: bool = False,
        include_sessions: bool = False
) -> models.User:
    statement = select(models.User).where(models.User.id == user_id)
    if include_profile:
        statement.options(selectinload(models.User.profile))
    if include_credentials:
        statement.options(selectinload(models.User.credentials))
    if include_sessions:
        statement.options(selectinload(models.User.sessions))

    user = (await database_session.execute(statement)).scalar()

    if user is None:
        raise ItemNotFoundError()

    return user


def add_user(database_session: AsyncSession, user: models.User):
    database_session.add(user)


def delete_user(database_session: AsyncSession, user_id: int):
    database_session.delete(models.User(id=user_id))


async def check_credentials(database_session: AsyncSession, credentials: schemas.UserCredentials) -> bool:
    statement = select(func.count()).select_from(
        models.UserCredentials
    ).where(
        models.UserCredentials.email == credentials.email
    ).where(
        models.UserCredentials.hashed_password == utils.sha256(credentials.password)
    )

    count = (await database_session.execute(statement)).scalar()

    return count > 0


async def get_user_by_credentials(
        database_session: AsyncSession,
        credentials: schemas.UserCredentials
) -> models.User | None:
    statement = select(models.UserCredentials).where(models.UserCredentials.email == credentials.email).where(
        models.UserCredentials.hashed_password == utils.sha256(credentials.password)
    )

    return (await database_session.execute(statement)).scalar().user


def create_session(
        database_session: AsyncSession, user_id: int, lifetime: timedelta
) -> tuple[str, models.UserSession]:
    token = secrets.token_hex(32)
    session = models.UserSession(
        user_id=user_id,
        hashed_token=utils.sha256(token),
        expires_on=datetime.now() + lifetime
    )
    database_session.add(session)
    return token, session
