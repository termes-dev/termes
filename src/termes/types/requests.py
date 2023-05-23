from pydantic import BaseModel

from termes.types.account import UserCredentials, UserProfile


class AuthenticationRequest(BaseModel):
    credentials: UserCredentials


class RegistrationRequest(BaseModel):
    credentials: UserCredentials
    profile: UserProfile
