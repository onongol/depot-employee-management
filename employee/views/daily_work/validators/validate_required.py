from django.utils.translation import gettext_lazy as _


def validate_required(selected_employee_ids, selected_work_ids, work_date, type_work, amounts):
    """Validate required fields and amounts for daily work entry."""
    errors = []

    # Check for required selections
    if not selected_employee_ids:
        errors.append(_("Please select at least one employee."))
    if not selected_work_ids:
        errors.append(_("Please select at least one work."))
    if not work_date or not type_work:
        errors.append(_("Please select work date, type work."))

    # Check for missing amounts for any selected work 
    missing_amounts = [wid for wid in selected_work_ids if not amounts.get(wid)]

    # If there are missing amounts, add an error message
    if missing_amounts:
        errors.append(
            _("Please fill in the amount for selected work(s).")
        )

    return errors
