import pandas as pd
from pathlib import Path
from parser.models.items import Item
from parser.utils.logger import get_logger
from parser.storage.base import set_up

logger = get_logger(__name__)

def save_to_csv(items: list[Item], path: Path | str):
    df = set_up(items, path)
    df.to_csv(path, index=False, encoding="utf-8-sig")

    logger.info("Сохранено: %d записей в %s", len(items), path)