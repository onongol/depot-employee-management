from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmployeeContext:
    employees: Any
    selected_department: str | None
    employee_id: str | None
    employee_name: str | None
    job_title: str | None
    order_by: str | None
    direction: str | None
    job_titles: list[str] = field(default_factory=list)
