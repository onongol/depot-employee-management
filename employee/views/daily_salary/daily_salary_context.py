from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class DailySalaryContext:
    daily_salaries: Any
    department: Optional[str]
    employee_id: Optional[str]
    employee_name: Optional[str]
    job_title: Optional[str]
    salary_date: Optional[str]
    record_date: Optional[str]
    order_by: Optional[str]
    direction: Optional[str]
    job_titles: List[str] = field(default_factory=list)
