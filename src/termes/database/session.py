import secrets
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from termes import utils
from termes.application import settings
from termes.errors import ItemNotFoundError
from termes.models import UserSession


async def get_session(database_session: AsyncSession, session_id: int) -> UserSession:
    session = await database_session.get(UserSession, session_id)

    if session is None:
        raise ItemNotFoundError()

    return session


async def generate_session(database_session: AsyncSession, user_id: int) -> tuple[UserSession, str]:
    token = secrets.token_hex(settings.SESSION_TOKEN_LENGTH)
    session = UserSession(
        user_id=user_id,
        hashed_token=utils.sha256(token, salt=settings.TOKEN_HASH_SALT),
        expires_on=datetime.now() + timedelta(seconds=settings.SESSION_LIFETIME)
    )
    database_session.add(session)
    await database_session.flush()
    return session, token


async def find_session_by_token(database_session: AsyncSession, token: str) -> UserSession:
    stmt = select(UserSession).where(UserSession.hashed_token == utils.sha256(token, salt=settings.TOKEN_HASH_SALT))

    session = (await database_session.execute(stmt)).scalar()

    if session is None:
        raise ItemNotFoundError()

    return session
