from django.utils.translation import gettext_lazy as _


def get_employees_preview(pieceworks, limit=10):
    '''
    This code generates a concise, human-readable summary of employees involved in piecework records for use in bulk operation messages. It limits the number of displayed employees and adds a tail if there are more, improving message clarity and user experience
    '''
    pieceworks_count = len(pieceworks)

    emp_preview = [
        f"{pw.employee.employee_id}/{pw.employee.name or ''}"
        for pw in pieceworks[:limit]
    ]
    emp_tail = "" if pieceworks_count <= limit else _(" … and %(n)s more") % {"n": pieceworks_count - limit}

    employees_summary =  ", ".join(emp_preview) + (emp_tail or "")

    return employees_summary, pieceworks_count
