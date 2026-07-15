from enum import Enum

from pydantic import BaseModel, Field


class UrlStatus(str, Enum):
    OK = "OK"
    REDIRECT = "Redirect"
    CLIENT_ERROR = "Client Error"
    SERVER_ERROR = "Server Error"
    TIMEOUT = "Timeout"
    CONNECTION_ERROR = "Connection Error"
    SSL_ERROR = "SSL Error"
    UNKNOWN_ERROR = "Unknown Error"


class StatusCategory(str, Enum):
    SUCCESS = "success"
    REDIRECT = "redirect"
    CLIENT_ERROR = "client_error"
    SERVER_ERROR = "server_error"
    TIMEOUT = "timeout"
    ERROR = "error"


class UrlsRequest(BaseModel):
    urls: list[str] = Field(
        description="Список URL для проверки."
    )


class UrlResult(BaseModel):
    url: str = Field(
        description="Проверяемый URL."
    )

    status_code: int | None = Field(
        default=None,
        description="HTTP-статус ответа."
    )

    response_time: float | None = Field(
        default=None,
        description="Время ответа в миллисекундах."
    )

    status: UrlStatus = Field(
        description="Текстовое описание результата."
    )

    category: StatusCategory = Field(
        description="Категория для отображения на фронтенде."
    )