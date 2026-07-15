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
        description="List of URLs to check"
    )


class UrlResult(BaseModel):
    url: str = Field(
        description="URL being checked"
    )

    status_code: int | None = Field(
        default=None,
        description="HTTP response status"
    )

    response_time: float | None = Field(
        default=None,
        description="Response time"
    )

    status: UrlStatus = Field(
        description="Textual description of the result"
    )

    category: StatusCategory = Field(
        description="Category for display on the frontend"
    )