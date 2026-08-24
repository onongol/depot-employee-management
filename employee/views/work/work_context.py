from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkContext:
    works: Any
    selected_department: str | None
    job_title: str | None
    work_name: str | None
    type_wagon: str | None
    order_by: str | None
    direction: str | None
    job_titles: list[str] = field(default_factory=list)
    type_wagons: list[str] = field(default_factory=list)
