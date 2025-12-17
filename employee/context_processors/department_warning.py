def needs_department_warning(request):
    """Provide a flag when selected_department is empty and current page needs a department."""
    pages_requiring_department = {
        'employee_list',
        'work_list',
        'daily_salary_list',
        'daily_work_list',
        'piecework_list',
        'employee_salary_list',
        'wagon_list',
    }
    url_name = getattr(getattr(request, 'resolver_match', None), 'url_name', None)
    selected_department = request.GET.get('department') or request.session.get('department')
    return {'needs_department_warning': (not selected_department) and (url_name in pages_requiring_department)}
