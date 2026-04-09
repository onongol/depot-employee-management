from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class WagonContext:
    daily_works: Any
    selected_department: Optional[str]
    wagon_number: Optional[str]
    type_wagon: Optional[str]
    work_name: Optional[str]
    type_work: Optional[str]
    range_date: Optional[str]
    group: Optional[str]
    month: Optional[int]
    year: Optional[int]
    month_period: Optional[str]
    order_by: Optional[str]
    direction: Optional[str]
    detail_group: bool = False
    month_group: bool = False
    year_group: bool = False
    show_wagon: bool = False
    type_wagons: List[str] = field(default_factory=list)
    type_works: List[str] = field(default_factory=list)
