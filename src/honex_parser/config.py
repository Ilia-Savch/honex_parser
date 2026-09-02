from dataclasses import dataclass

AVITO_BASE_URL = "https://www.avito.ru"
AVITO_CATEGORY_PATH = "zapchasti_i_aksessuary"


@dataclass(frozen=True)
class SearchConfig:
    """Настройки поиска, используемые для создания URL-адресов поиска Avito."""

    region_slug: str = "moskva_i_mo"
    condition_value: str = "new"
    sort_value: str = "price_asc"
    max_results_per_article: int = 5

