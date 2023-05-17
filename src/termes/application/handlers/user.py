from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from termes.application.dependencies import get_database_session
from termes.schemas import UserResponse, ErrorResponse

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse | ErrorResponse)
async def get(database_session: Annotated[AsyncSession, Depends(get_database_session)], user_id: int):
    pass
