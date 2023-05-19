from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from termes import database, models, utils, schemas
from termes.application import settings
from termes.application.dependencies import get_database_session
from termes.schemas import RegistrationResponse, RegistrationRequest

router = APIRouter(
    responses={
        409: {
            "description": "User with this email(or username) is already registered"
        }
    },
    tags=["Registration"]
)


@router.post("/", response_model=RegistrationResponse)
async def registration(
        database_session: Annotated[AsyncSession, Depends(get_database_session)],
        request: RegistrationRequest
):
    if await database.check_credentials(database_session, request.credentials.email):
        raise HTTPException(409, "User with this email is already registered")
    if request.profile.username and await database.check_username(database_session, request.profile.username):
        raise HTTPException(409, "User with this username is already registered")

    user = models.User(
        credentials=models.UserCredentials(
            email=request.credentials.email,
            hashed_password=utils.sha256(request.credentials.password, salt=settings.PASSWORD_HASH_SALT)
        ),
        profile=models.UserProfile(**request.profile.dict())
    )

    await database.add_user(database_session, user)
    await database_session.commit()

    return schemas.RegistrationResponse(user=schemas.User.from_orm(user))
