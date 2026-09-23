"""Настройка логирования для парсера.

Все параметры берутся из parser.config.settings.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from parser.config import settings

def get_logger(name: str, console: bool | None = None) -> logging.Logger:
    """
    Возвращает настроенный логгер.

    Параметры (уровень, формат, файл, ротация) берутся из settings.
    Повторные вызовы с тем же name не создают дублирующих обработчиков.

    Args:
        name: имя логгера, обычно __name__.
        console: переопределить вывод в консоль (по умолчанию — из settings).
    """
    logger = logging.getLogger(name)

    # если логгер уже настроен — не трогаем
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level)
    logger.propagate = False  # не передаём в корневой логгер, чтобы не было дублей

    formatter = logging.Formatter(settings.log_format, datefmt=settings.log_datefmt)

    # --- файловый обработчик ---
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_dir / settings.log_file,
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # --- консольный обработчик ---
    # console=None → берём из настроек; console=True/False → явное переопределение
    use_console = settings.log_console if console is None else console
    if use_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger