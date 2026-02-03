from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class DailyWorkPieceworkCreateContext:
    form: Any
    object_type: str
    employees: Any
    works: Any
    today: Any
    work_date: Any
    errors: List[str] = field(default_factory=list)
    selected_department: Optional[str] = None
    cancel_url: Optional[str] = None
    existing_pieceworks: List[dict] = field(default_factory=list)
    job_titles: List[str] = field(default_factory=list)
    type_wagons: List[str] = field(default_factory=list)
    show_wagon: bool = False
