from pydantic import BaseModel

from .user import UserCredentials, UserProfile


class RegistrationRequest(BaseModel):
    credentials: UserCredentials
    profile: UserProfile


class AuthenticationRequest(BaseModel):
    credentials: UserCredentials
