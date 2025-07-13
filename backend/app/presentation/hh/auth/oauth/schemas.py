from pydantic import BaseModel, HttpUrl


class AuthorizeURLSchema(BaseModel):
    url: HttpUrl


class ErrorResponse(BaseModel):
    error: str