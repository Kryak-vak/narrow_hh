from fastapi import APIRouter, Depends

from app.application.users.auth.oauth import HHOAuthService
from app.presentation.users.deps import get_hh_auth_service
from app.presentation.users.schemas import AuthorizeURLSchema, ErrorResponse
from core.config import settings

router = APIRouter(
    prefix="/hh",
    tags=["hh_auth"]
)


@router.post(
    "/oauth/start", 
    response_model=AuthorizeURLSchema
)
async def oauth_start(
        telegram_user_id: int,
        hh_auth_service: HHOAuthService = Depends(get_hh_auth_service)
    ) -> dict:
    """
    HH Oauth start.
    """
    authorize_url = await hh_auth_service.create_authorize_url(telegram_user_id)

    return AuthorizeURLSchema(url=authorize_url)


@router.post(
    f"{settings.HH_REDIRECT_URI}",
    responses={
        400: {"model": ErrorResponse, "description": "User denied access"}
    }
)
async def oauth_callback(
        code: str,
        state: str,
        error: str = None,
        hh_auth_service: HHOAuthService = Depends(get_hh_auth_service)
    ) -> dict:
    """
    HH Oauth callback.
    """
    if error == "access_denied":  # TODO Add custom error with error_handler
        return {"error": "access denied by user"}

    access_token = await hh_auth_service.get_tokens(code, state)

    return {"access_token": access_token}
