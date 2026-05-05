from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional


@dataclass
class PostData:
    work_date: Optional[date]
    type_work: Optional[str]
    job_title: Optional[str]
    wagon_number: Optional[str]
    selected_employee_ids: List[str]
    selected_work_ids: List[str]
    amounts: Dict[str, str]

