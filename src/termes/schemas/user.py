from datetime import datetime

from pydantic import BaseModel


class UserProfile(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    created_at: datetime
    profile: UserProfile

    class Config:
        orm_mode = True