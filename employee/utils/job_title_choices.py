from collections.abc import Iterable
from itertools import chain


def build_job_title_choices(employees: Iterable, works: Iterable) -> list[str]:
    """Build a sorted list of unique job titles from employees and works."""
    return sorted(
        {
            title
            for title in chain(
                (employee.job_title for employee in employees),
                (work.job_title for work in works),
            )
            if title
        }
    )
