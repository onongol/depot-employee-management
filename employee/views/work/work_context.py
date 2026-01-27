from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class WorkContext:
    works: Any
    selected_department: Optional[str]
    job_title: Optional[str]
    work_name: Optional[str]
    type_wagon: Optional[str]
    order_by: Optional[str]
    direction: Optional[str]
    job_titles: List[str] = field(default_factory=list)
    type_wagons: List[str] = field(default_factory=list)
