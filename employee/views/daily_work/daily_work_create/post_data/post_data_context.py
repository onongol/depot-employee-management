from dataclasses import dataclass
from datetime import date


@dataclass
class PostData:
    work_date: date | None
    type_work: str | None
    job_title: str | None
    wagon_number: str | None
    selected_employee_ids: list[str]
    selected_work_ids: list[str]
    amounts: dict[str, str]

