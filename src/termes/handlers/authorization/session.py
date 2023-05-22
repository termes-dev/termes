from fastapi import APIRouter

router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized"
        }
    }
)


@router.get("/session")
async def current_session():
    pass


@router.get("/session/{session_id}")
async def session_by_id(session_id: int):
    pass
