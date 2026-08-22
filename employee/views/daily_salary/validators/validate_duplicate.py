from django.utils.translation import gettext_lazy as _


def validate_daily_salary_duplicate(emp_id, emp, existing_records, salary_date, errors):
    if emp_id in existing_records:
        errors.append(
            _("Record for %(employee)s on %(date)s already exists.")
            % {"employee": str(emp), "date": salary_date}
        )
        return True
    return False
