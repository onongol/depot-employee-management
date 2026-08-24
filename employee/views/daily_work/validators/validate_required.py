from django.utils.translation import gettext_lazy as _


def validate_required(
    selected_employee_ids, selected_work_ids, work_date, type_work, amounts
):
    """Validate required fields and amounts for daily work entry."""
    errors = []

    # Check for required selections
    if not selected_employee_ids:
        errors.append(_("Select at least one employee."))
    if not selected_work_ids:
        errors.append(_("Select at least one work."))
    if not work_date or not type_work:
        errors.append(_("Select work date and type."))

    # Check for missing amounts for any selected work
    missing_amounts = [
        work_id for work_id in selected_work_ids if not amounts.get(work_id)
    ]

    # If there are missing amounts, add an error message
    if missing_amounts:
        errors.append(_("Enter an amount for each selected work entry."))

    return errors
