from app.infrastructure.database import AbstractSQLAlchemyRepository


class UserRepository(
        AbstractSQLAlchemyRepository
    ):
    pass


class UserTokenRepository(AbstractSQLAlchemyRepository):
    pass