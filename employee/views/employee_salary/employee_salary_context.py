from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmployeeSalaryContext:
    employees: Any
    employee_id: str | None
    employee_name: str | None
    selected_department: str | None
    job_title: str | None
    wagon_number: str | None
    month: int | None
    year: int | None
    month_period: str | None
    group: str | None
    order_by: str | None
    direction: str | None
    show_wagon: bool = False
    total_group: bool = False
    wagon_group: bool = False
    wagon_mode: bool = False
    job_titles: list[str] | None = field(default_factory=list)
