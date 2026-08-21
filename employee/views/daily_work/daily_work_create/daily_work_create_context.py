from dataclasses import dataclass, field
from typing import Any


@dataclass
class DailyWorkPieceworkCreateContext:
    form: Any
    object_type: str
    employees: Any
    works: Any
    today: Any
    work_date: Any
    errors: list[str] = field(default_factory=list)
    selected_department: str | None = None
    cancel_url: str | None = None
    existing_pieceworks: list[dict] = field(default_factory=list)
    job_titles: list[str] = field(default_factory=list)
    type_wagons: list[str] = field(default_factory=list)
    show_wagon: bool = False
