"""Основная логика запуска парсера."""

from parser.config import settings, BOOKS_JSON, BOOKS_CSV
from parser.utils.logger import get_logger
from parser.scrapers.catalogue import scrape_catalogue
from parser.storage.csv_storage import save_to_csv
from parser.storage.json_storage import save_to_json, read_from_json
from parser.analysis.analyze_json import save_analytics

logger = get_logger(__name__)

def run() -> int:
    """Делает работу. Возвращает код выхода (0 — успех)."""
    logger.info("Старт парсера. base_url=%s", settings.base_url)

    items = scrape_catalogue(max_pages=1)
    for index, item in enumerate(items):
        logger.debug("Номер книги - %d, название - %s, рейтинг - %s, цена - %s %s", index, item.title, item.rating, item.price, item.currency)

    save_to_json(items, BOOKS_JSON)

    df = read_from_json(BOOKS_JSON)
    save_analytics(df)

    logger.info("Готово")
    return 0

def main() -> None:
    """Обёртка для entry-point."""
    raise SystemExit(run())

if __name__ == "__main__":
    main()