from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


def iter_rows(qs, department):
    """Generate rows for DailyWork export based on department."""
    show_wagon = department in ALLOWED_WAGON_DEPARTMENTS
    for i, dw in enumerate(qs, start=1):
        row = [
            i,
            getattr(dw.work, 'work_name', '') or "",
            dw.job_title or "",
            dw.type_work or "",
        ]
        if show_wagon:
            row.append(dw.wagon_number_display or "")
            row.append(dw.type_wagon_display or "")
        row.extend([
            dw.amount or 0,
            dw.amount_time or 0,
            dw.amount_price or 0,
            dw.work_date or "",
        ])
        yield row
