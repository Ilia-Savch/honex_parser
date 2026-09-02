from honex_parser.parser import Listing

MOSCOW_REGION_LOCATIONS = (
    "москва",
    "московская область",
    "одинцово",
    "балашиха",
    "химки",
    "мытищи",
    "люберцы",
    "красногорск",
    "подольск",
    "королёв",
    "королев",
    "домодедово",
    "видное",
    "реутов",
    "долгопрудный",
    "лобня",
    "пушкино",
    "щелково",
    "серпухов",
    "коломна",
    "электросталь",
    "ногинск",
)

def get_price(listing: Listing) -> int:
    """Возвращает цену для сортировки."""

    if listing.price is None:
        raise ValueError("Нельзя сортировать объявление без цены")

    return listing.price


def select_top_listings(
    listings: list[Listing],
    limit: int,
) -> list[Listing]:
    """Отбирает самые дешёвые объявления по требованиям ТЗ."""

    unique_listings = remove_duplicates(listings)

    suitable_listings = [
        listing
        for listing in unique_listings
        if listing.price is not None
        and is_new_condition(listing)
        and is_moscow_region(listing)
    ]

    return sorted(suitable_listings, key=get_price)[:limit]


def remove_duplicates(listings: list[Listing]) -> list[Listing]:
    """Убирает дубли объявлений по ссылке."""

    seen_urls: set[str] = set()
    result: list[Listing] = []

    for listing in listings:
        if listing.url in seen_urls:
            continue

        seen_urls.add(listing.url)
        result.append(listing)

    return result


def is_new_condition(listing: Listing) -> bool:
    """Проверяет, что объявление относится к новым товарам."""

    condition = listing.condition.lower()

    return condition == "новое"


def is_moscow_region(listing: Listing) -> bool:
    """Проверяет, что объявление находится в Москве или МО."""

    location = listing.city_or_region.lower()
    url = listing.url.lower()

    return any(
        allowed_location in location or allowed_location in url
        for allowed_location in MOSCOW_REGION_LOCATIONS
    )