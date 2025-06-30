from django.shortcuts import redirect

from employee.utils.select_department import get_selected_department

DEPARTMENTS = [
    'Механик', 
    'Авто хяналтын бүс (АКП)', 
    'Засвар 1', 
    'Засвар 2', 
    'Хос дугуй', 
    'Тэргэнцэр', 
    'Автоугсраа'
]

def set_department(request):
    """Set the department in the user's session."""
    department = get_selected_department(request)
    if department in DEPARTMENTS:
        request.session['department'] = department
    else:
        request.session['department'] = None
    return redirect(request.META.get('HTTP_REFERER', '/'))
