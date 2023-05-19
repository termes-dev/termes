from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from termes import database
from termes.application.dependencies import get_database_session
from termes.errors import ItemNotFoundError
from termes.schemas import AuthenticationResponse, AuthenticationRequest, UserSession

router = APIRouter(
    responses={
        403: {
            "description": "Invalid credentials"
        }
    },
    tags=["Authentication"]
)


@router.post("/", response_model=AuthenticationResponse)
async def authentication(
        database_session: Annotated[AsyncSession, Depends(get_database_session)],
        request: AuthenticationRequest
):
    try:
        credentials = await database.find_credentials(
            database_session, request.credentials.email, request.credentials.password
        )
    except ItemNotFoundError:
        raise HTTPException(403, "Invalid credentials")

    session, token = await database.generate_session(database_session, credentials.user_id)
    await database_session.commit()

    return AuthenticationResponse(
        session=UserSession.from_orm(session),
        token=token
    )
