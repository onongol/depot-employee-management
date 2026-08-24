from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass
class PieceworkContext:
    pieceworks: Any
    selected_department: str | None
    employee_code: str | None
    employee_name: str | None
    job_title: str | None
    work_name: str | None
    type_work: str | None
    wagon_number: str | None
    type_wagon: str | None
    # range_date is the raw box contents, kept for redisplay; the filter reads
    # the parsed bounds.
    range_date: str | None
    date_from: date | None
    date_to: date | None
    record_date: date | None
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
    type_wagons: list[str] | None = field(default_factory=list)
    years: list[str] | None = field(default_factory=list)
