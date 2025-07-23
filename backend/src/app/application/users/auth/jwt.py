from datetime import datetime, timedelta
from typing import Any, cast
from uuid import UUID

import jwt

from src.app.application.users.auth.dto import JWTEntity, JWTType
from src.app.utils import datetime_now
from src.config.app import app_config
from src.config.jwt import jwt_config


class JWTManager:
    def __get_access_expire_date(self) -> datetime:
        return datetime_now() + timedelta(minutes=jwt_config.access_expire)

    def __get_refresh_expire_date(self) -> datetime:
        return datetime_now() + timedelta(days=jwt_config.refresh_expire)

    def create_access_token(self, user_id: UUID) -> str:
        token = JWTEntity(
            user_id=str(user_id),
            type=JWTType.ACCESS,
            expire=str(self.__get_access_expire_date()),
        )
        return jwt.encode(
            token.model_dump(),
            app_config.secret_key,
            algorithm=jwt_config.algorithm,
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        token = JWTEntity(
            user_id=str(user_id),
            type=JWTType.REFRESH,
            expire=str(self.__get_refresh_expire_date()),
        )

        return jwt.encode(
            token.model_dump(),
            app_config.secret_key,
            algorithm=jwt_config.algorithm,
        )

    def decode_token(self, token: str) -> dict[str, Any]:
        return cast(
            dict[str, Any],
            jwt.decode(
                token,
                app_config.secret_key,
                algorithms=[jwt_config.algorithm],
            ),
        )
