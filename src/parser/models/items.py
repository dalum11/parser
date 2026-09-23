"""Модель данных для одного элемента"""

from dataclasses import dataclass, asdict
from dataclasses import field
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class Item:
    title: str
    url: str
    price: Decimal | None = None
    currency: str = "GBP"
    in_stock: bool = True
    rating: int | None = None          # 1..5
    image_url: str | None = None
    description: str | None = None
    category: str | None = None
    sku: str | None = None
    source: str | None = None
    scraped_at: datetime = datetime.now().isoformat()


    def to_dict(self): 
        data = asdict(self)
        data["price"] = str(self.price)
        data["scraped_at"] = self.scraped_at
        return data
        