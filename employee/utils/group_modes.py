from employee.constants.constants import (
    GROUP_DEFAULT,
    GROUP_MONTH,
    GROUP_WAGON,
    GROUP_YEAR,
)


def normalize_group(group: str | None) -> str:
    return (group or "").strip()


def is_detail_group(group: str | None) -> bool:
    return normalize_group(group) == GROUP_DEFAULT


def is_grouped(group: str | None) -> bool:
    return normalize_group(group) in (GROUP_MONTH, GROUP_YEAR)


def is_month_group(group: str | None) -> bool:
    return normalize_group(group) == GROUP_MONTH


def is_year_group(group: str | None) -> bool:
    return normalize_group(group) == GROUP_YEAR


def is_wagon_group(group: str | None) -> bool:
    return normalize_group(group) == GROUP_WAGON
