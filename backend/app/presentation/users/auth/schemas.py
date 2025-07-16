from pydantic import BaseModel, HttpUrl, ValidationError, model_validator


class StartAuthPayloadSchema(BaseModel):
    state: str
    notify_url: HttpUrl | None = None
    redirect_url: HttpUrl | None = None

    @model_validator(mode='before')
    def check_exactly_one(cls, data):
        notify_url, redirect_url = data.get('notify_url'), data.get('redirect_url')  # type: ignore[attr-defined]
        if bool(notify_url) + bool(redirect_url) != 1:
            raise ValidationError("Exactly one of 'notify_url' or 'redirect_url' must be provided.")
        return data