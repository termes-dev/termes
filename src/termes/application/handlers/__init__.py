from fastapi import APIRouter

from . import authentication, registration, account, user

router = APIRouter()
router.include_router(authentication.router, prefix="/authentication")
router.include_router(registration.router, prefix="/registration")
router.include_router(account.router, prefix="/account")
router.include_router(user.router, prefix="/user")
