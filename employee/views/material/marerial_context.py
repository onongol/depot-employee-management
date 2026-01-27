from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class MaterialContext:
    daily_works: Any
    work_name: Optional[str]
    type_material: Optional[str]
    range_date: Optional[str]
    order_by: Optional[str]
    direction: Optional[str]
