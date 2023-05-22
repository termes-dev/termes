from fastapi import APIRouter

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


@router.post("/registration")
async def registration():
    pass
