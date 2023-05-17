from pydantic import BaseModel

from .user import User


class UserResponse(BaseModel):
    user: User


class RegistrationResponse(BaseModel):
    user: User


class AuthenticationResponse(BaseModel):
    session: UserSession
    token: str
