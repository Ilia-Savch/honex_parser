from pathlib import Path

from honex_parser.avito import build_search_url, fetch_html
from honex_parser.config import SearchConfig
from honex_parser.exporter import save_to_csv
from honex_parser.parser import parse_listings
from honex_parser.processing import select_top_listings
from honex_parser.results import (
    ResultRow,
    build_error_row,
    build_found_rows,
    build_not_found_row,
)


ARTICLES = ["223112R020", "233002F700"]
FIXTURES_DIR = Path("tests/fixtures")
OUTPUT_PATH = "result/result.csv"


def main() -> None:
    """Запускает полный пайплайн и сохраняет результат в CSV."""

    config = SearchConfig()
    rows = collect_result_rows(ARTICLES, config)

    save_to_csv(rows, OUTPUT_PATH)


def collect_result_rows(
    articles: list[str],
    config: SearchConfig,
) -> list[ResultRow]:
    """Собирает итоговые строки для всех артикулов."""

    rows: list[ResultRow] = []

    for article in articles:
        rows.extend(collect_article_rows(article, config))

    return rows


def collect_article_rows(
    article: str,
    config: SearchConfig,
) -> list[ResultRow]:
    """Собирает итоговые строки для одного артикула."""

    search_query = article
    url = build_search_url(article, config)

    fetch_result = fetch_html(url)
    html = fetch_result.html

    if not fetch_result.ok:
        html = read_fixture(article)

        if html is None:
            return [
                build_error_row(
                    article=article,
                    search_query=search_query,
                    url=url,
                    error=fetch_result.error or "страница не получена",
                )
            ]

    if html is None:
        return [
            build_error_row(
                article=article,
                search_query=search_query,
                url=url,
                error="HTML не найден",
            )
        ]

    listings = parse_listings(html)
    top_listings = select_top_listings(
        listings=listings,
        limit=config.max_results_per_article,
    )

    if not top_listings:
        return [build_not_found_row(article=article, search_query=search_query)]

    return build_found_rows(
        article=article,
        search_query=search_query,
        listings=top_listings,
    )


def read_fixture(article: str) -> str | None:
    """Читает сохранённую HTML-страницу для артикула."""

    fixture_path = FIXTURES_DIR / f"html_{article}.html"
    if not fixture_path.exists():
        return None

    return fixture_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    main()

