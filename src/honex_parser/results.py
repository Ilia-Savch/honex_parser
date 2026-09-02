from dataclasses import dataclass
from datetime import datetime

from honex_parser.parser import Listing


@dataclass(frozen=True)
class ResultRow:
    """Строка итоговой таблицы."""

    article: str
    search_query: str
    title: str
    price: int | None
    city_or_region: str
    condition: str
    url: str
    price_rank: int | None
    checked_at: str
    status: str
    error: str


def build_found_rows(
    article: str,
    search_query: str,
    listings: list[Listing],
) -> list[ResultRow]:
    """Создаёт строки для найденных объявлений."""

    checked_at = get_checked_at()
    rows: list[ResultRow] = []

    for index, listing in enumerate(listings, start=1):
        rows.append(
            ResultRow(
                article=article,
                search_query=search_query,
                title=listing.title,
                price=listing.price,
                city_or_region=listing.city_or_region,
                condition=listing.condition,
                url=listing.url,
                price_rank=index,
                checked_at=checked_at,
                status="найдено",
                error="",
            )
        )

    return rows


def build_not_found_row(article: str, search_query: str) -> ResultRow:
    """Создаёт строку, если подходящих объявлений нет."""

    return ResultRow(
        article=article,
        search_query=search_query,
        title="",
        price=None,
        city_or_region="",
        condition="",
        url="",
        price_rank=None,
        checked_at=get_checked_at(),
        status="не найдено",
        error="",
    )


def build_error_row(
    article: str,
    search_query: str,
    url: str,
    error: str,
) -> ResultRow:
    """Создаёт строку при ошибке загрузки страницы."""

    return ResultRow(
        article=article,
        search_query=search_query,
        title="",
        price=None,
        city_or_region="",
        condition="",
        url=url,
        price_rank=None,
        checked_at=get_checked_at(),
        status="ошибка",
        error=error,
    )


def get_checked_at() -> str:
    """Возвращает дату и время проверки."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

