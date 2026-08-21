from dataclasses import dataclass, field
from typing import Any


@dataclass
class DailySalaryCreateContext:
    form: Any
    object_type: str
    employees: Any
    errors: list[str] = field(default_factory=list)
    today: Any = None
    selected_department: str | None = None
    cancel_url: str | None = None
    job_titles: list[str] = field(default_factory=list)
    existing_daily_salaries: list[dict] = field(default_factory=list)
