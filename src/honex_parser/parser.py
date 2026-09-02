from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from bs4.element import Tag

from honex_parser.config import AVITO_BASE_URL


@dataclass(frozen=True)
class Listing:
    """Одно объявление из выдачи Avito."""

    title: str
    price: int | None
    city_or_region: str
    condition: str
    url: str


def _get_text(card: Tag, selector: str) -> str:
    """Безопасно достаёт текст по CSS-селектору."""

    element = card.select_one(selector)
    if element is None:
        return ""

    return element.get_text(" ", strip=True)


def _get_url(card: Tag) -> str:
    """Достаёт абсолютную ссылку на объявление."""

    link = card.select_one('a[data-marker="item-title"]')
    if link is None:
        return ""

    href = link.get("href")
    if not isinstance(href, str):
        return ""

    return urljoin(AVITO_BASE_URL, href)


def _get_condition(card: Tag) -> str:
    """Пытается найти состояние товара в тексте карточки."""

    text = card.get_text(" ", strip=True).lower()

    if "новое" in text or "новый" in text:
        return "новое"

    return ""

def parse_price(price_text: str) -> int | None:
    """Преобразует цену в число."""

    digits = "".join(char for char in price_text if char.isdigit())

    if not digits:
        return None

    return int(digits)

def parse_listings(html: str) -> list[Listing]:
    """Достаёт объявления из HTML-страницы Avito."""

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select('[data-marker="item"]')

    listings: list[Listing] = []

    for card in cards:
        title = _get_text(card, '[data-marker="item-title"]')
        price_text = _get_text(card, '[data-marker="item-price"]')
        city_or_region = _get_text(card, '[data-marker="item-address"]')
        if not city_or_region:
            city_or_region = _get_text(card, '[data-marker="item-location"]')
        url = _get_url(card)
        condition = _get_condition(card)

        if not title or not url:
            continue

        listings.append(
            Listing(
                title=title,
                price=parse_price(price_text),
                city_or_region=city_or_region,
                condition=condition,
                url=url,
            )
        )

    return listings
