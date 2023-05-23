from fastapi import APIRouter, HTTPException

from termes.server import services
from termes.types.requests import RegistrationRequest
from termes.types.responses import RegistrationResponse

router = APIRouter(
    responses={
        403: {
            "description": "Not allowed to register"
        },
        409: {
            "description": "Email (or username) is already used"
        }
    }
)


@router.post("/registration", response_model=RegistrationResponse)
async def registration(request: RegistrationRequest):
    response = await services.account.registration(request)

    if isinstance(response, RegistrationResponse):
        return response

    raise HTTPException(response.code, response.detail)
