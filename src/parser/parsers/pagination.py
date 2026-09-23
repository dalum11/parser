"""Утилита для извлечения ссылки на следующую страницу"""

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from parser.utils.logger import get_logger

logger = get_logger(__name__)

def get_next_page_url(html: str, current_url: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.select_one("li.next > a")
    if next_link is None or not next_link.get("href"):
        return None

    next_url = urljoin(current_url, next_link["href"])
    logger.debug("Следующая страница: %s", next_url)
    return next_url