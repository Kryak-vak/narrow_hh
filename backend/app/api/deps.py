from collections.abc import Generator
from functools import partial
from typing import Annotated, Type

from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_service(service_cls, session: SessionDep):
    repository = service_cls.repository_class(session)
    return service_cls(session, repository)


def service_dep(service_cls):
    return Depends(partial(get_service, service_cls))