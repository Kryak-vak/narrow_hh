from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.csrf import StateManager
from app.application.hh.auth.dto import HeadHunterUserDTO, OauthTokenDTO
from app.application.hh.auth.oauth import HHOAuthService
from app.application.users.auth.dto import JWTEntity, JWTPairDTO, JWTType
from app.application.users.auth.jwt import JWTManager
from app.application.users.dto import (
    HeadHunterTokenCreateDTO,
    HeadHunterTokenDTO,
    HeadHunterTokenUpdateDTO,
    UserCreateDTO,
    UserDTO,
    UserRefreshTokenCreateDTO,
)
from app.infrastructure.clients import HHAsyncClient
from app.infrastructure.database.users.repositories import (
    HeadHunterTokenRepository,
    UserRepository,
    UserTokenRepository,
)
from app.utils import datetime_now


class UserAuthService:
    def __init__(
            self, session: AsyncSession, 
            user_repo: UserRepository,
            user_token_repo: UserTokenRepository,
            hh_token_repo: HeadHunterTokenRepository,
            hh_auth_service: HHOAuthService,
            state_manager: StateManager,
            jwt_manager: JWTManager,
        ):
        self.session = session
        self.user_repo = user_repo
        self.user_token_repo = user_token_repo
        self.hh_token_repo = hh_token_repo
        self.hh_auth_service = hh_auth_service
        self.state_manager = state_manager
        self.jwt_manager = jwt_manager
        
        self.hh_client = HHAsyncClient
    
    async def start_auth_hh(
            self, state: str,
            interface_redirect_url: str
        ) -> str:
        await self.state_manager.set_state_ex(state, str(interface_redirect_url))

        return self.hh_auth_service.get_user_authorize_url(state, interface_redirect_url)
    
    async def login(self, authorization_code: str, state: str):
        interface_redirect_url = await self.state_manager.get_state(state)

        user_dto = await self._get_or_create_user_hh(authorization_code, interface_redirect_url)
        token_pair = self._create_token_pair(user_dto.id)

        await self.__create_refresh_token_in_database(token_pair.refresh_token, user_dto.id)

        return token_pair
    
    async def refresh(self, token: str) -> JWTPairDTO:
        jwt_entity = JWTEntity(
            **self.jwt_manager.decode_token(token)
        )
        await self.__check_token_is_valid(token, jwt_entity, JWTType.REFRESH)

        user_dto = await self.user_repo.get(id=jwt_entity.user_id)
        if user_dto is None:
            raise(RuntimeError("invalid user_id in token"))  # TODO add custom exception

        return self._create_token_pair(user_dto.id)
    
    def _create_token_pair(self, user_id: UUID) -> JWTPairDTO:
        access_token = self.jwt_manager.create_access_token(user_id)
        refresh_token = self.jwt_manager.create_refresh_token(user_id)

        return JWTPairDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def _get_or_create_user_hh(
            self, authorization_code: str,
            interface_redirect_url: str
        ) -> UserDTO:
        hh_oauth_tokens_dto = await self._authorize_user_hh(
            authorization_code, interface_redirect_url
        )
        hh_user_dto = await self._get_hh_user_info(hh_oauth_tokens_dto.access_token)
        
        user_dto = await self.user_repo.get(hh_user_id=hh_user_dto.id)
        if user_dto is None:
            user_dto = await self._create_user_with_hh_token(hh_user_dto.id, hh_oauth_tokens_dto)
        else:
            await self._update_user_hh_token(user_dto.id, hh_oauth_tokens_dto)
        
        return user_dto
    
    async def _create_user_with_hh_token(self, hh_user_id: str, hh_oauth_tokens_dto: OauthTokenDTO):
        user_dto = await self.user_repo.create(
            UserCreateDTO(hh_user_id=hh_user_id)
        )

        await self.hh_token_repo.create(
            HeadHunterTokenCreateDTO(
                user_id=user_dto.id,
                **hh_oauth_tokens_dto.model_dump()
            )
        )

        await self.session.commit()
        user_dto = await self.user_repo.refresh(user_dto)

        return user_dto
    
    async def _update_user_hh_token(
            self, user_id: UUID,
            hh_oauth_tokens_dto: OauthTokenDTO
        ) -> HeadHunterTokenDTO:
        user_hh_token_dto = await self.hh_token_repo.get(with_related=False, user_id=user_id)
        if user_hh_token_dto is None:
            raise ValueError(
                f"HeadHunterToken for user {user_id} not found"
            )  # TODO add custom exception

        hh_token_dto = await self.hh_token_repo.update(
            user_hh_token_dto.id,
            HeadHunterTokenUpdateDTO(**hh_oauth_tokens_dto.model_dump())
        )

        return hh_token_dto
    
    async def _authorize_user_hh(
            self, authorization_code: str,
            interface_redirect_url: str,
        ) -> OauthTokenDTO:
        hh_oauth_tokens_dto = await self.hh_auth_service.authorize_user(
            authorization_code,
            interface_redirect_url
        )

        return hh_oauth_tokens_dto
    
    async def _get_hh_user_info(self, access_token: str) -> HeadHunterUserDTO:
        async with self.hh_client() as client:
            hh_user_data = await client.make_me_request(access_token)
            
        return HeadHunterUserDTO(**hh_user_data)

    async def __create_refresh_token_in_database(self, refresh_token: str, user_id: UUID) -> None:
        refresh_token_create_dto = UserRefreshTokenCreateDTO(id=refresh_token, user_id=user_id)
        await self.user_token_repo.create(refresh_token_create_dto)
    
    async def __check_token_is_valid(
        self, token: str, jwt_entity: JWTEntity, expected_token_type: JWTType
    ) -> None:
        if jwt_entity.type != expected_token_type:
            raise RuntimeError("JWTInvalidTokenTypeException")

        if datetime_now() > datetime.strptime(jwt_entity.expire, "%Y-%m-%d %H:%M:%S.%f%z"):
            raise RuntimeError("JWTTokenExpiredException")

        if expected_token_type == JWTType.REFRESH:
            await self.__check_token_not_in_blacklist(token)

    async def __check_token_not_in_blacklist(self, token: str) -> None:
        pass

    async def __add_token_to_blacklist(self, token: str, jwt_entity: JWTEntity) -> None:
        pass





