from parser.utils.logger import get_logger
import pandas as pd
from pathlib import Path
from parser.config import ANALYSIS_XLSX

logger = get_logger(__name__)


def save_analytics(df: pd.DataFrame, path: Path = ANALYSIS_XLSX) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        _average_by_category(df).to_excel(writer, sheet_name="avg_price_by_category")
        _count_by_category(df).to_excel(writer, sheet_name="count_by_category")
        _in_stock_percent(df).to_excel(writer, sheet_name="in_stock_by_category")
        _top_rated(df).to_excel(writer, sheet_name="top_rated_books")

    logger.info("Аналитика сохранена: %s", path)
    

def _average_by_category(df: pd.DataFrame):
    average_amount_by_category = df.groupby("category")["price"].mean().round(2)
    return average_amount_by_category

def _count_by_category(df: pd.DataFrame):
    books_count_by_category = df["category"].value_counts()
    return books_count_by_category

def _in_stock_percent(df: pd.DataFrame):
    in_stock_percent_by_category = (df.groupby("category")["in_stock"].mean() * 100).round(2)
    return in_stock_percent_by_category

def _top_rated(df: pd.DataFrame, count: int = 10):
    most_popular_books = df.nlargest(count, "rating")[["title", "rating", "price", "category"]]
    return most_popular_books


    
