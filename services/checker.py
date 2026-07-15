import asyncio
import time
from urllib.parse import urlparse
import httpx
from schemas.url import StatusCategory, UrlResult, UrlStatus



REQUEST_TIMEOUT_SECONDS: int = 10

DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "SEOStatusChecker/1.0",
}


def normalize_url(url: str) -> str | None:
   
    normalized_url = url.strip().lower()

    if not normalized_url:
        return None

    parsed_url = urlparse(normalized_url)

    if not parsed_url.scheme:
        normalized_url = f"https://{normalized_url}"

    return normalized_url


def prepare_urls(urls: list[str]) -> list[str]:

    prepared_urls: list[str] = []
    seen_urls: set[str] = set()

    for url in urls:
        if (normalized_url := normalize_url(url)) is None:
            continue

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        prepared_urls.append(normalized_url)

    return prepared_urls


def get_status_info(
    status_code: int,
) -> tuple[UrlStatus, StatusCategory]:


    if 200 <= status_code < 300:
        return UrlStatus.OK, StatusCategory.SUCCESS

    if 300 <= status_code < 400:
        return UrlStatus.REDIRECT, StatusCategory.REDIRECT

    if 400 <= status_code < 500:
        return UrlStatus.CLIENT_ERROR, StatusCategory.CLIENT_ERROR

    if 500 <= status_code < 600:
        return UrlStatus.SERVER_ERROR, StatusCategory.SERVER_ERROR

    # Все остальные коды считаем неизвестными.
    return UrlStatus.UNKNOWN_ERROR, StatusCategory.ERROR


def create_error_result(
    *,
    url: str,
    status: UrlStatus,
    category: StatusCategory,
) -> UrlResult:
    

    return UrlResult(
        url=url,
        status_code=None,
        response_time=None,
        status=status,
        category=category,
    )


async def check_url(
    client: httpx.AsyncClient,
    url: str,
) -> UrlResult:
    

    start_time = time.perf_counter()

    try:
        response = await client.get(
            url=url,
            follow_redirects=True,
        )

        response_time = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        status_code = response.status_code
        status, category = get_status_info(status_code)

        return UrlResult(
            url=url,
            status_code=status_code,
            response_time=response_time,
            status=status,
            category=category,
        )

    except httpx.TimeoutException:
        return create_error_result(
            url=url,
            status=UrlStatus.TIMEOUT,
            category=StatusCategory.TIMEOUT,
        )

    except httpx.ConnectError:
        return create_error_result(
            url=url,
            status=UrlStatus.CONNECTION_ERROR,
            category=StatusCategory.ERROR,
        )

    except httpx.RequestError:
        return create_error_result(
            url=url,
            status=UrlStatus.UNKNOWN_ERROR,
            category=StatusCategory.ERROR,
        )

    except Exception:
        return create_error_result(
            url=url,
            status=UrlStatus.UNKNOWN_ERROR,
            category=StatusCategory.ERROR,
        )


async def check_urls(
    urls: list[str],
) -> list[UrlResult]:
    

    prepared_urls = prepare_urls(urls)

    async with httpx.AsyncClient(
        headers=DEFAULT_HEADERS,
        timeout=httpx.Timeout(REQUEST_TIMEOUT_SECONDS),
    ) as client:

        tasks = (
            check_url(client, url)
            for url in prepared_urls
        )

        return await asyncio.gather(*tasks)