from dataclasses import dataclass
from typing import Any


@dataclass
class MaterialContext:
    daily_works: Any
    work_name: str | None
    type_material: str | None
    range_date: str | None
    order_by: str | None
    direction: str | None
