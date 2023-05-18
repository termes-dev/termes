from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from termes.application.dependencies import get_database_session
from termes.schemas import UserResponse

router = APIRouter(
    tags=["User"]
)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(database_session: Annotated[AsyncSession, Depends(get_database_session)], user_id: int):
    pass
