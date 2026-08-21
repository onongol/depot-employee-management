from dataclasses import dataclass, field
from typing import Any


@dataclass
class WagonContext:
    daily_works: Any
    selected_department: str | None
    wagon_number: str | None
    type_wagon: str | None
    work_name: str | None
    type_work: str | None
    range_date: str | None
    group: str | None
    month: int | None
    year: int | None
    month_period: str | None
    order_by: str | None
    direction: str | None
    detail_group: bool = False
    month_group: bool = False
    year_group: bool = False
    show_wagon: bool = False
    type_wagons: list[str] = field(default_factory=list)
    type_works: list[str] = field(default_factory=list)
