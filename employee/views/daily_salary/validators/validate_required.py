from django.utils.translation import gettext_lazy as _


def validate_required(selected_ids, salary_date, hours_per_day):
    """Validate required fields for daily salary creation."""
    errors = []

    # Check if any employees are selected
    if not selected_ids:
        errors.append(_("Please select at least one employee."))

    # Validate required fields
    if not salary_date or not hours_per_day:
        errors.append(_("Please select date and hours!"))

    return errors
