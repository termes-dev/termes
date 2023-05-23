from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class UserSession(BaseModel):
    id: int
    created_at: datetime
    expires_on: datetime


class UserProfile(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None


class User(BaseModel):
    id: int
    created_at: int
    profile: UserProfile
