from pydantic import BaseModel, HttpUrl


class AbstractInputSchema(BaseModel):
    pass


class AbstractOutputSchema(BaseModel):
    pass


class URLSchema(AbstractInputSchema):
    url: HttpUrl


class ErrorResponse(AbstractOutputSchema):
    error: str