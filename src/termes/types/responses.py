from pydantic import BaseModel

from termes.types.account import UserSession, User


class ErrorResponse(BaseModel):
    code: int
    detail: str


class AuthenticationResponse(BaseModel):
    session: UserSession
    token: str


class RegistrationResponse(BaseModel):
    user: User
