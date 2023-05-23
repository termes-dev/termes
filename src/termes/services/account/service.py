from typing import Final

from termes.services.account.types import (
    ServiceAuthenticationRequest,
    ServiceAuthenticationResponse,
    ServiceRegistrationRequest,
    ServiceRegistrationResponse
)
from termes.services.service import Service
from termes.types.requests import AuthenticationRequest, RegistrationRequest
from termes.types.responses import AuthenticationResponse, ErrorResponse, RegistrationResponse

AUTHENTICATION_ENDPOINT: Final[str] = "authentication"
REGISTRATION_ENDPOINT: Final[str] = "registration"


class AccountService(Service):
    async def authentication(self, request: AuthenticationRequest) -> AuthenticationResponse | ErrorResponse:
        response = await self.request(
            AUTHENTICATION_ENDPOINT,
            ServiceAuthenticationRequest(
                data=request
            ),
            ServiceAuthenticationResponse
        )

        if response.status == 200:
            return response.data

        return response.error

    async def registration(self, request: RegistrationRequest) -> RegistrationResponse | ErrorResponse:
        response = await self.request(
            REGISTRATION_ENDPOINT,
            ServiceRegistrationRequest(
                data=request
            ),
            ServiceRegistrationResponse
        )

        if response.status == 200:
            return response.data

        return response.error
