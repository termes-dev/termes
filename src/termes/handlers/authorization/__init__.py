from fastapi import APIRouter

from termes.handlers.authorization import authentication, registration, session

router = APIRouter(tags=["Authorization"])
router.include_router(authentication.router)
router.include_router(registration.router)
router.include_router(session.router)
