from fastapi import APIRouter

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


@router.post("/authentication")
async def authentication():
    pass
