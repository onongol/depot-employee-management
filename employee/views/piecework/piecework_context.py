from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class PieceworkContext:
    pieceworks: Any
    selected_department: Optional[str]
    employee_id: Optional[str]
    employee_code: Optional[str]
    employee_name: Optional[str]
    job_title: Optional[str]
    work_name: Optional[str]
    type_work: Optional[str]
    wagon_number: Optional[str]
    type_wagon: Optional[str]
    range_date: Optional[str]
    record_date: Optional[str]
    group: Optional[str]
    selected_year: Optional[str]
    month: Optional[int]
    year: Optional[int]
    month_period: Optional[str]
    order_by: Optional[str]
    direction: Optional[str]
    show_wagon: bool = False
    detail_group: bool = False
    month_group: bool = False
    year_group: bool = False
    job_titles: Optional[List[str]] = field(default_factory=list)
    type_works: Optional[List[str]] = field(default_factory=list)
    type_wagons: Optional[List[str]] = field(default_factory=list)
    years: Optional[List[str]] = field(default_factory=list)
