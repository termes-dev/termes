from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from termes.application.dependencies import get_database_session
from termes.schemas import RegistrationResponse, RegistrationRequest

router = APIRouter(
    tags=["Registration"]
)


@router.post("/", response_model=RegistrationResponse)
async def registration(
        database_session: Annotated[AsyncSession, Depends(get_database_session)],
        request: RegistrationRequest
):
    pass

