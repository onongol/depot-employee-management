from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, DEFAULT_WAGON_TYPE


def get_type_wagon_filter_values(
    department,
    source_model: str = "work",  # 'work' | 'piecework'
    always_include_default: bool = False,
):
    """
    Build a distinct list of type_wagon values for a filter widget.

    Parameters:
        department (str):
            The base department code selected by the user (must be in ALLOWED_WAGON_DEPARTMENTS).
        source_model (str):
            'work'      -> pull current type_wagon values from Work (live reference data).
            'piecework' -> pull snapshot values from Piecework.type_wagon (historical state).
        always_include_default (bool):
            If True, always prepend DEFAULT_WAGON_TYPE (placeholder for NULL).
            If False, prepend it only when there are NULL entries in the underlying data.
    """
    # Fast exit if department is not provided or not allowed to have wagon filtering.
    if not department or department not in ALLOWED_WAGON_DEPARTMENTS:
        return []

    # Dynamically choose the source model and the department lookup path.
    deps = [department]

    # Dynamically choose the source model and the department lookup path.
    if source_model == "piecework":
        # Snapshot (historical) source: use Piecework entries and follow employee -> department.
        from employee.models import Piecework as Model

        dep_lookup = "employee__department__in"
        field = "type_wagon"
    else:
        # Default / live source: use Work reference data, department lives directly on Work.
        from employee.models import Work as Model

        dep_lookup = "department__in"
        field = "type_wagon"

    # Base queryset filtered by department(s).
    qs = Model.objects.filter(**{dep_lookup: deps})

    # Detect if there are any NULL values; those map to DEFAULT_WAGON_TYPE in the filter UI.
    has_null = qs.filter(**{f"{field}__isnull": True}).exists()

    # Collect non-NULL distinct values only; NULL is represented separately (placeholder).
    values = list(
        qs.exclude(**{f"{field}__isnull": True})
        .values_list(field, flat=True)
        .distinct()
        .order_by()
    )

    # Prepend placeholder if forced or if NULL values actually exist.
    if always_include_default or has_null:
        return [DEFAULT_WAGON_TYPE] + values

    return values
