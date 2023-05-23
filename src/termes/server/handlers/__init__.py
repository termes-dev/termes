from fastapi import APIRouter

from termes.server.handlers import authorization

router = APIRouter()
router.include_router(authorization.router)
