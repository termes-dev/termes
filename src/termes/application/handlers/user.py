from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_database_session
from ... import models, database, schemas
from ...errors import ItemNotFoundError

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_by_id(user_id: int, database_session: Annotated[AsyncSession, Depends(get_database_session)]):
    try:
        user: models.User = await database.get_user(database_session, user_id, include_profile=True)
        if user.deleted:
            raise HTTPException(status_code=410, detail="User deleted")
        return schemas.UserResponse(user=schemas.User.from_orm(user))
    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
