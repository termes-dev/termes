from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from termes.application.dependencies import get_database_session
from termes.schemas import AuthenticationResponse, ErrorResponse, AuthenticationRequest

router = APIRouter()


@router.post("/", response_model=AuthenticationResponse | ErrorResponse)
async def authentication(
        database_session: Annotated[AsyncSession, Depends(get_database_session)],
        request: AuthenticationRequest
):
    pass
