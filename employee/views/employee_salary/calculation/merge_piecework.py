from collections.abc import Iterable, Mapping


def merge_piecework(
    salary_data,
    *,
    piecework_groups: Iterable[Mapping],
    group_by_wagon: bool,
) -> None:
    """
    Build the final salary rows for rendering/export from aggregated salary_data.
    It maps employee IDs back to Employee objects and computes per-row totals for each (employee, year, month, wagon).
    """
    
    for group in piecework_groups:
        wagon = group.get("wagon_number") if group_by_wagon else None
        key = (
            group["employee"],
            group["work_date__year"],
            group["work_date__month"],
            wagon,
        )
        salary_data[key]["total_piecework_amount"] = (
            group.get("total_piecework_amount") or 0
        )
        salary_data[key]["total_piecework_time"] = (
            group.get("total_piecework_time") or 0
        )
