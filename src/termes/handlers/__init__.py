from fastapi import APIRouter

from termes.handlers import authorization

router = APIRouter()
router.include_router(authorization.router)
