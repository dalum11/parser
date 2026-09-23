from pathlib import Path
from parser.models.items import Item
from parser.utils.logger import get_logger
from parser.storage.base import set_up
import pandas as pd

logger = get_logger(__name__)

def save_to_json(items: list[Item], path: Path | str) -> None:
    df = set_up(items, path)
    df.to_json(path, orient="records", force_ascii=False, indent=2)

    logger.info("Сохранено: %d записей в %s", len(items), path)

def read_from_json(path: Path) -> pd.DataFrame:
    df = pd.read_json(path, orient="records")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").astype("Int64")
    return df