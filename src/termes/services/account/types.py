from termes.services.types import ServiceRequest, ServiceResponse
from termes.types.requests import AuthenticationRequest, RegistrationRequest
from termes.types.responses import AuthenticationResponse, RegistrationResponse


class ServiceAuthenticationRequest(ServiceRequest):
    data: AuthenticationRequest


class ServiceAuthenticationResponse(ServiceResponse):
    data: AuthenticationResponse


class ServiceRegistrationRequest(ServiceRequest):
    data: RegistrationRequest


class ServiceRegistrationResponse(ServiceResponse):
    data: RegistrationResponse
