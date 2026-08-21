from dataclasses import dataclass, field
from typing import Any


@dataclass
class DailyWorkContext:
    daily_works: Any
    selected_department: str | None
    job_title: str | None
    work_name: str | None
    type_work: str | None
    wagon_number: str | None
    type_wagon: str | None
    type_material: str | None
    range_date: str | None
    record_date: str | None
    group: str | None
    selected_year: str | None
    month: int | None
    year: int | None
    month_period: str | None
    order_by: str | None
    direction: str | None
    show_wagon: bool = False
    detail_group: bool = False
    month_group: bool = False
    year_group: bool = False
    job_titles: list[str] | None = field(default_factory=list)
    type_works: list[str] | None = field(default_factory=list)
    type_materials: list[str] | None = field(default_factory=list)
    type_wagons: list[str] | None = field(default_factory=list)
    years: list[str] | None = field(default_factory=list)
