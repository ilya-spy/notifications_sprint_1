from src.frontend.api.schemas.base import BaseAPISchema
from pydantic import Field


class DefaultSuccessResponse(BaseAPISchema):
    """Общий успешный ответ"""

    status: str = Field("success")
