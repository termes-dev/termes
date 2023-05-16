from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_database_session
from ... import database, schemas, models

router = APIRouter()


@router.post("/", response_model=schemas.RegistrationResponse)
async def registration(
        database_session: Annotated[AsyncSession, Depends(get_database_session)],
        request: schemas.RegistrationRequest
):
    if await database.check_credentials(database_session, credentials=request.credentials):
        raise HTTPException(status_code=400, detail="Email is already used")

    user = models.User(
        profile=models.UserProfile(**request.profile.dict())
    )

    database.add_user(database_session, user)
    await database_session.commit()

    return schemas.RegistrationResponse(user=user)


