from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class MaterialContext:
    daily_works: Any
    work_name: str | None
    type_material: str | None
    # range_date is the raw box contents, kept for redisplay; the filter reads
    # the parsed bounds.
    range_date: str | None
    date_from: date | None
    date_to: date | None
    order_by: str | None
    direction: str | None
