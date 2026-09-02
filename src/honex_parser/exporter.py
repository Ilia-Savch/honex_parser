import csv
from pathlib import Path

from honex_parser.results import ResultRow


CSV_COLUMNS = [
    "article",
    "search_query",
    "title",
    "price",
    "city_or_region",
    "condition",
    "url",
    "price_rank",
    "checked_at",
    "status",
    "error",
]


def save_to_csv(rows: list[ResultRow], output_path: str) -> None:
    """Сохраняет строки результата в CSV-файл."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()

        for row in rows:
            writer.writerow(result_row_to_dict(row))


def result_row_to_dict(row: ResultRow) -> dict[str, str | int | None]:
    """Преобразует ResultRow в словарь для CSV."""

    return {
        "article": row.article,
        "search_query": row.search_query,
        "title": row.title,
        "price": row.price,
        "city_or_region": row.city_or_region,
        "condition": row.condition,
        "url": row.url,
        "price_rank": row.price_rank,
        "checked_at": row.checked_at,
        "status": row.status,
        "error": row.error,
    }