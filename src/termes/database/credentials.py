from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from termes import utils
from termes.application import settings
from termes.models import UserCredentials


async def check_credentials(database_session: AsyncSession, email: str, password: str | None = None) -> bool:
    statement = select(func.count()).select_from(UserCredentials).where(UserCredentials.email == email)

    if password is not None:
        statement.where(UserCredentials.hashed_password == utils.sha256(password, salt=settings.PASSWORD_HASH_SALT))

    count = (await database_session.execute(statement)).scalar()

    return count > 0


async def find_credentials(database_session: AsyncSession, email: str, password: str) -> UserCredentials | None:
    statement = select(UserCredentials).where(
        UserCredentials.email == email
    ).where(
        UserCredentials.hashed_password == utils.sha256(password, salt=settings.PASSWORD_HASH_SALT)
    )

    return (await database_session.execute(statement)).scalar()


async def get_credentials(database_session: AsyncSession, user_id: int) -> UserCredentials | None:
    statement = select(UserCredentials).where(UserCredentials.user_id == user_id)
    return (await database_session.execute(statement)).scalar()
