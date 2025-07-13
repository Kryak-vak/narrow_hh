from fastapi import APIRouter

from app.presentation.hh.auth.oauth.router import router as hh_oauth_router

router = APIRouter()
router.include_router(hh_oauth_router)
