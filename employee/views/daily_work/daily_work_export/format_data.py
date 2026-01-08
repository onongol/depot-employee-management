from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_MONTH, GROUP_YEAR


def _get(item, key, default=""):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def iter_rows(qs, department, group=None):
    """Generate rows for DailyWork export (detailed or grouped)."""
    show_wagon = department in ALLOWED_WAGON_DEPARTMENTS

    for i, dw in enumerate(qs, start=1):
        is_grouped = group in (GROUP_MONTH, GROUP_YEAR)

        work_name = _get(dw, "work_name") if is_grouped else getattr(getattr(dw, "work", None), "work_name", "") or ""
        job_title = _get(dw, "job_title", "") or ""
        type_work = _get(dw, "type_work", "") or ""

        row = [i, work_name, job_title, type_work]

        if show_wagon:
            if is_grouped:
                row.append(_get(dw, "wagon_number", "") or "")
                row.append(_get(dw, "type_wagon", "") or "")
            else:
                row.append(_get(dw, "wagon_number_display", "") or "")
                row.append(_get(dw, "type_wagon_display", "") or "")

        if is_grouped:
            row.extend([
                _get(dw, "total_amount", 0) or 0,
                _get(dw, "total_time", 0) or 0,
                _get(dw, "total_price", 0) or 0,
            ])
            if group == GROUP_MONTH:
                row.extend([_get(dw, "month", "") or "", _get(dw, "year", "") or ""])
            else:
                row.append(_get(dw, "year", "") or "")
        else:
            row.extend([
                _get(dw, "amount", 0) or 0,
                _get(dw, "amount_time", 0) or 0,
                _get(dw, "amount_price", 0) or 0,
                _get(dw, "work_date", "") or "",
            ])

        yield row
