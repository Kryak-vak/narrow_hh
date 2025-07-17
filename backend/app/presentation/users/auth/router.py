from fastapi import APIRouter, Depends

from app.application.users.auth.user import UserAuthService
from app.presentation.schemas import ErrorResponse, URLSchema
from app.presentation.users.auth.deps import get_user_auth_service
from app.presentation.users.auth.schemas import StartAuthPayloadSchema
from config.hh import hh_config

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/login_via_hh", 
    response_model=URLSchema
)
async def login_via_hh(
        payload: StartAuthPayloadSchema,
        user_auth_service: UserAuthService = Depends(get_user_auth_service)
    ) -> dict:
    """
    HH Oauth start.
    """
    authorize_url = await user_auth_service.start_auth_hh(
        state=payload.state,
        notify_url=payload.notify_url,
        redirect_url=payload.redirect_url
    )

    return URLSchema(url=authorize_url)


@router.post(
    f"{hh_config.redirect_uri}",
    responses={
        400: {"model": ErrorResponse, "description": "User denied access"}
    }
)
async def oauth_callback(
        code: str,
        state: str,
        error: str = None,
        user_auth_service: UserAuthService = Depends(get_user_auth_service)
    ) -> dict:
    """
    HH Oauth callback.
    """
    if error == "access_denied":  # TODO Add custom error with error_handler
        return {"error": "access denied by user"}

    access_token = await user_auth_service.get_tokens(code, state)

    return {"access_token": access_token}
