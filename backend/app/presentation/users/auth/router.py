from fastapi import APIRouter, Depends

from app.application.users.auth.user import UserAuthService
from app.presentation.schemas import URLSchema
from app.presentation.users.auth.deps import get_user_auth_service
from app.presentation.users.auth.schemas import (
    AuthCallbackPayloadSchema,
    AuthStartPayloadSchema,
    TokenPairSchema,
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/login_via_hh/start", 
    response_model=URLSchema
)
async def login_via_hh_start(
        payload: AuthStartPayloadSchema,
        user_auth_service: UserAuthService = Depends(get_user_auth_service)
    ) -> dict:
    """
    Get a custom Headhunter's authorize url.
    """
    authorize_url = await user_auth_service.start_auth_hh(
        state=payload.state,
        interface_redirect_url=payload.redirect_url
    )

    return URLSchema(url=authorize_url)


@router.post(
    "/login_via_hh/callback",
    response_model=TokenPairSchema,
)
async def login_via_hh_callback(
        payload: AuthCallbackPayloadSchema,
        user_auth_service: UserAuthService = Depends(get_user_auth_service)
    ) -> dict:
    """
    Get access tokens from HeadHunter's authorization code.
    """
    token_pair_dto = await user_auth_service.login(payload.code, payload.state)

    return TokenPairSchema(
        token_pair_dto.access_token,
        token_pair_dto.refresh_token,
    )
