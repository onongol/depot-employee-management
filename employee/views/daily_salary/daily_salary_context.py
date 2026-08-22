from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass
class DailySalaryContext:
    daily_salaries: Any
    selected_department: str | None
    employee_id: str | None
    employee_code: str | None
    employee_name: str | None
    job_title: str | None
    salary_date: date | None
    record_date: date | None
    order_by: str | None
    direction: str | None
    job_titles: list[str] = field(default_factory=list)
