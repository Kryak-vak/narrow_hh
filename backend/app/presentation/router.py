from fastapi import APIRouter

from app.presentation.users.auth.router import router as user_auth_router

router = APIRouter()
router.include_router(user_auth_router)
