from pydantic import BaseModel

from termes.schemas.user import UserCredentials, UserProfile


class RegistrationRequest(BaseModel):
    credentials: UserCredentials
    profile: UserProfile


class AuthenticationRequest(BaseModel):
    credentials: UserCredentials
