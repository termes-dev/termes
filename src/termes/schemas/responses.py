from pydantic import BaseModel

from .user import User


class UserResponse(BaseModel):
    user: User
