from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from termes import utils
from termes.application import settings
from termes.errors import ItemNotFoundError
from termes.models import UserCredentials


async def check_credentials(database_session: AsyncSession, email: str, password: str | None = None) -> bool:
    stmt = select(func.count()).select_from(UserCredentials).where(UserCredentials.email == email)

    if password is not None:
        stmt.where(UserCredentials.hashed_password == utils.sha256(password, salt=settings.PASSWORD_HASH_SALT))

    count = (await database_session.execute(stmt)).scalar()

    return count > 0


async def find_credentials(database_session: AsyncSession, email: str, password: str) -> UserCredentials:
    stmt = select(UserCredentials).where(
        UserCredentials.email == email
    ).where(
        UserCredentials.hashed_password == utils.sha256(password, salt=settings.PASSWORD_HASH_SALT)
    )

    credentials = (await database_session.execute(stmt)).scalar()

    if credentials is None:
        raise ItemNotFoundError()

    return credentials


async def get_credentials(database_session: AsyncSession, user_id: int) -> UserCredentials:
    credentials = await database_session.get(UserCredentials, user_id)

    if credentials is None:
        raise ItemNotFoundError()

    return credentials
