from django.shortcuts import redirect
from django.views.decorators.http import require_POST

DEPARTMENTS = [
    'Механик', 
    'Авто хяналтын бүс (АКП)', 
    'Засвар 1', 
    'Засвар 2', 
    'Хос дугуй', 
    'Тэргэнцэр', 
    'Автоугсраа'
]


@require_POST
def set_department(request):
    """Set the department in the user's session."""
    department = request.POST.get('department')
    if department in DEPARTMENTS:
        request.session['department'] = department
    else:
        request.session['department'] = None
    return redirect(request.META.get('HTTP_REFERER', '/'))
