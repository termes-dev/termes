from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from termes import database
from termes.application.dependencies import get_database_session
from termes.errors import ItemNotFoundError
from termes.schemas import UserResponse, User

router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized (invalid session token or session expired)"
        },
        410: {
            "description": "User deleted"
        }
    },
    tags=["Account"]
)


@router.get("/", response_model=UserResponse)
async def get_account_user(
        database_session: Annotated[AsyncSession, Depends(get_database_session)],
        x_token: Annotated[str, Header()]
):
    try:
        session = await database.find_session_by_token(database_session, x_token)
    except ItemNotFoundError:
        raise HTTPException(401, "Unauthorized")

    if datetime.now() >= session.expires_on:
        raise HTTPException(401, "Unauthorized")

    user = await database.get_user(database_session, session.user_id, include_profile=True)

    if user.deleted:
        raise HTTPException(410, "User deleted")

    return UserResponse(user=User.from_orm(user))


