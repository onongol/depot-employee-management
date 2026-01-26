from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class DailySalaryCreateContext:
    form: Any
    object_type: str
    employees: Any
    errors: List[str] = field(default_factory=list)
    today: Any = None
    selected_department: Optional[str] = None
    cancel_url: Optional[str] = None
    job_titles: List[str] = field(default_factory=list)
