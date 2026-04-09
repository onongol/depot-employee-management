from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class EmployeeSalaryContext:
    employees: Any
    employee_id: Optional[str]
    employee_name: Optional[str]
    selected_department: Optional[str]
    job_title: Optional[str]
    wagon_number: Optional[str]
    month: Optional[int]
    year: Optional[int]
    month_period: Optional[str]
    group: Optional[str]
    order_by: Optional[str]
    direction: Optional[str]
    show_wagon: bool = False
    total_group: bool = False
    wagon_group: bool = False
    wagon_mode: bool = False
    job_titles: Optional[List[str]] = field(default_factory=list)
