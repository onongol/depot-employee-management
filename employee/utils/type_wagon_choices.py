from employee.constants.constants import DEFAULT_WAGON_TYPE


def build_type_wagon_choices(works, *, show_wagon: bool) -> list[str]:
    if not show_wagon:
        return []

    type_wagon_values = sorted(
        {work.type_wagon for work in works if work.type_wagon is not None}
    )
    empty_type_wagon = any(work.type_wagon is None for work in works)

    if empty_type_wagon:
        return [DEFAULT_WAGON_TYPE] + type_wagon_values

    return type_wagon_values
