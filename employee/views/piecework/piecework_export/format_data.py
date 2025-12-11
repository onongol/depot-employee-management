from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


def iter_rows(qs, department):
    """Generate rows for Pieceworks export based on department."""
    show_wagon = department in ALLOWED_WAGON_DEPARTMENTS
    for i, pw in enumerate(qs, start=1):
        row = [
            i,
            pw.employee.employee_id or "",
            pw.employee.name or "",
            pw.department or "",
            pw.job_title or "",
            pw.work.work_name or "",
            pw.type_work or "",
        ]
        if show_wagon:
            row.append(pw.wagon_number_display or "")
            row.append(pw.type_wagon_display or "")
        row.extend([
            pw.amount or 0,
            pw.amount_time or 0,
            pw.amount_price or 0,
            pw.work_date or "",
        ])
        yield row
