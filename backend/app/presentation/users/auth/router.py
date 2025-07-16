from fastapi import APIRouter, Depends

from app.application.users.auth.user import UserAuthService
from app.presentation.schemas import ErrorResponse, URLSchema
from app.presentation.users.auth.deps import get_user_auth_service
from app.presentation.users.auth.schemas import StartAuthPayloadSchema
from config.hh import hh_config

router = APIRouter(
    prefix="/hh",
    tags=["hh_auth"]
)


@router.post(
    "/oauth/start", 
    response_model=URLSchema
)
async def oauth_start(
        payload: StartAuthPayloadSchema,
        user_auth_service: UserAuthService = Depends(get_user_auth_service)
    ) -> dict:
    """
    HH Oauth start.
    """
    authorize_url = await user_auth_service.start_auth(
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

    access_token = await hh_auth_service.get_tokens(code, state)

    return {"access_token": access_token}
