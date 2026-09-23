"""Настройки парсера — читаются из переменных окружения и .env."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_DIR = PROJECT_ROOT / "src" / "parser"
DATA_DIR = PROJECT_DIR / "data"
INPUT_DIR = DATA_DIR / "input_data"
OUTPUT_DIR = DATA_DIR / "output_data"
LOGS_DIR = PROJECT_ROOT / "logs"

BOOKS_JSON = OUTPUT_DIR / "books.json"
BOOKS_CSV = OUTPUT_DIR / "books.csv"
ANALYSIS_XLSX = OUTPUT_DIR / "analysis.xlsx"

for d in (INPUT_DIR, OUTPUT_DIR, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)

def _load_dotenv(path: Path = Path(".env")) -> None:
    """Простой парсер"""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
    
        os.environ.setdefault(key, value)

_load_dotenv() 

def _parse_log_level(value: str) -> int:
    """Принимает 'INFO', 'debug', '10' — возвращает числовой уровень logging."""
    value = value.strip().upper()
    if value.isdigit():
        return int(value)
    return getattr(logging, value, logging.INFO)

def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}

frozen=True
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://books.toscrape.com")
    request_timeout: float = float(os.getenv("REQUEST_TIMEOUT", "10.0"))
    user_agent: str = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (compatible; MyParser/1.0; +https://example.com/bot)",
    )

    log_level: int = _parse_log_level(os.getenv("LOG_LEVEL", "INFO"))
    log_dir: Path = Path(os.getenv("LOG_DIR", "logs"))
    log_file: str = os.getenv("LOG_FILE", "parser.log")
    log_format: str = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )
    log_datefmt: str = os.getenv("LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")
    log_max_bytes: int = int(os.getenv("LOG_MAX_BYTES", str(5 * 1024 * 1024)))
    log_backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "3"))
    log_console: bool = _parse_bool(os.getenv("LOG_CONSOLE", "true"))

settings = Settings()