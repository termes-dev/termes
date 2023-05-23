from fastapi import APIRouter, HTTPException

from termes.server import services
from termes.types.requests import AuthenticationRequest
from termes.types.responses import AuthenticationResponse

router = APIRouter(
    responses={
        401: {
            "description": "Incorrect credentials"
        },
        403: {
            "description": "Not allowed to authenticate"
        },
        410: {
            "description": "Account deleted"
        }
    }
)


@router.post("/authentication", response_model=AuthenticationResponse)
async def authentication(request: AuthenticationRequest):
    response = await services.account.authentication(request)

    if isinstance(response, AuthenticationResponse):
        return response

    raise HTTPException(response.code, response.detail)
