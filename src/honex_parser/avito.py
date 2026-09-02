import httpx

from dataclasses import dataclass
from urllib.parse import urlencode

from honex_parser.config import AVITO_BASE_URL, AVITO_CATEGORY_PATH, SearchConfig


@dataclass(frozen=True)
class FetchResult:
    """Результат получения страницы."""

    url: str
    ok: bool
    html: str | None = None
    status_code: int | None = None
    error: str | None = None


def _map_sort_to_avito_param(sort_value: str) -> str:
    sort_mapping = {
        "price_asc": "1",
    }

    return sort_mapping.get(sort_value, "1")

def _map_condition_to_avito_params(
    condition_value: str,
) -> dict[str, str] | None:
    condition_mapping = {
        "new": {"goods_condition": "new"},
    }

    return condition_mapping.get(condition_value)

def build_search_url(article: str, config: SearchConfig) -> str:
    """Генерация URL-адреса для поиска в Avito для одной статьи."""

    normalized_article = article.strip()
    if not normalized_article:
        raise ValueError("Артикул не может быть пустым")

    query_params = {
        "q": normalized_article,
        "s": _map_sort_to_avito_param(config.sort_value),
    }

    condition_params = _map_condition_to_avito_params(config.condition_value)
    if condition_params is not None:
        query_params.update(condition_params)

    encoded_params = urlencode(query_params)

    return (
        f"{AVITO_BASE_URL}/{config.region_slug}/"
        f"{AVITO_CATEGORY_PATH}?{encoded_params}"
    )

def fetch_html(url: str, timeout: float = 15.0) -> FetchResult:
    """Получает HTML страницы Avito."""

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }

    try:
        response = httpx.get(
            url,
            headers=headers,
            timeout=timeout,
            follow_redirects=True,
        )
    except httpx.TimeoutException:
        return FetchResult(url=url, ok=False, error="таймаут запроса")
    except httpx.RequestError as exc:
        return FetchResult(url=url, ok=False, error=f"ошибка запроса: {exc}")

    if response.status_code != 200:
        return FetchResult(
            url=url,
            ok=False,
            status_code=response.status_code,
            error=f"HTTP {response.status_code}",
        )

    html = response.text.strip()
    if not html:
        return FetchResult(
            url=url,
            ok=False,
            status_code=response.status_code,
            error="пустая страница",
        )

    if is_blocked_page(html):
        return FetchResult(
            url=url,
            ok=False,
            status_code=response.status_code,
            error="похоже на блокировку или CAPTCHA",
        )

    return FetchResult(
        url=url,
        ok=True,
        html=html,
        status_code=response.status_code,
    )

def is_blocked_page(html: str) -> bool:
    """Проверяет базовые признаки блокировки."""

    text = html.lower()

    return (
        "captcha" in text
        or "доступ ограничен" in text
        or "подтвердите, что вы не робот" in text
    )