from pydantic import BaseModel

from termes.schemas.user import User, UserSession


class ErrorResponse(BaseModel):
    code: int
    message: str


class UserResponse(BaseModel):
    user: User


class RegistrationResponse(BaseModel):
    user: User


class AuthenticationResponse(BaseModel):
    session: UserSession
    token: str
