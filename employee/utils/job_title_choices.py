def build_job_title_choices(employees, works) -> list[str]:
    return sorted(
        {
            job_title
            for job_title in [
                *(employee.job_title for employee in employees),
                *(work.job_title for work in works),
            ]
            if job_title
        }
    )
