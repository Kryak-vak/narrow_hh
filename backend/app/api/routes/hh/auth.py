from fastapi import APIRouter

from app.api.deps import service_dep
from app.core.config import settings
from app.services.hh import HHAuthService

router = APIRouter(
    prefix="/hh",
    tags=["hh_auth"]
)


@router.post("/oauth/start")
async def oauth_start(
        telegram_user_id: int,
        hh_auth_service: HHAuthService = service_dep(HHAuthService)
    ) -> dict:
    """
    HH Oauth start.
    """
    authorize_url = await hh_auth_service.create_authorize_url(telegram_user_id)

    return {"url": authorize_url}


@router.post(f"{settings.HH_REDIRECT_URI}")
async def oauth_callback(
        code: str,
        state: str,
        hh_auth_service: HHAuthService = service_dep(HHAuthService)
    ) -> dict:
    """
    HH Oauth callback.
    """
    access_token = await hh_auth_service.get_tokens(code, state)

    return {"access_token": access_token}
