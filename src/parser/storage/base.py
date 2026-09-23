from parser.models.items import Item
from pathlib import Path
import pandas as pd
from parser.utils.logger import get_logger

logger = get_logger(__name__)

def set_up(items: list[Item], path: Path | str) -> pd.DataFrame:
    if not items:
        logger.warning("Нечего сохранять в json")
        return
    
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    return pd.DataFrame([item.to_dict() for item in items])
