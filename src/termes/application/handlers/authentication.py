from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_database_session
from ... import schemas, database
from ...schemas import AuthenticationRequest

router = APIRouter()


@router.post("/", response_model=schemas.AuthenticationResponse)
async def authentication(
        database_session: Annotated[AsyncSession, Depends(get_database_session)],
        request: AuthenticationRequest
):
    user = database.get_user_by_credentials(database_session, request.credentials)

    if user is None:
        raise HTTPException(status_code=403, detail="Incorrect credentials")

    session