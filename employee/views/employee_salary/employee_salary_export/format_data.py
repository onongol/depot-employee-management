def iter_rows(qs):
    """Generate rows for Employee Salary export based on department."""
    for i, item in enumerate(qs, start=1):
        row = [
            i,
            item['employee'].employee_id or "",
            item['employee'].name or "",
            item['employee'].department or "",
            item['employee'].job_title or "",
            item['employee'].rank or "",
            item['total_piecework_time'] or 0,
            #item['total_salary_day'] or 0,
            item['total_piecework_amount'] or 0,
            #item['total_salary'] or 0,
            item['month'] or "",
            item['year'] or "",
        ]
        yield row
